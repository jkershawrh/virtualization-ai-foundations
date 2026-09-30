import { registerAdapter } from './adapters'
import healthyFixture from './fixtures/healthy.json'
import unavailableFixture from './fixtures/unavailable.json'
import type { LiveDataAdapter } from '../types'

type Condition = 'healthy' | 'model-unavailable'
type AdapterResult = Record<string, unknown> & {
  request_id: string
  source_state: string
  ai_participated: string
  model_id: string
  hardware: string
  category: string
  outcome: string
  authority: string
}

type AnalysisResponse = {
  request_id: string
  source_state: 'LIVE' | 'REHEARSAL' | 'OFFLINE'
  condition: Condition
  ai_participated: boolean
  model: { id: string; provider: string; hardware: string } | null
  result: { category: string; summary: string; rationale: string } | null
  validation: { schema_valid: boolean; category_valid: boolean }
  authority: { model: string; final_decision_owner: string; actions_permitted: string[] }
}

function flatten(response: AnalysisResponse): AdapterResult {
  return {
    request_id: response.request_id,
    source_state: response.source_state,
    ai_participated: response.ai_participated ? 'yes' : 'no',
    model_id: response.model?.id ?? 'none',
    hardware: response.model?.hardware ?? 'not invoked',
    category: response.result?.category ?? 'none',
    outcome: response.ai_participated
      ? response.validation.schema_valid && response.validation.category_valid ? 'Schema-valid advisory output' : 'Output rejected'
      : response.condition === 'healthy' && response.source_state === 'REHEARSAL'
        ? 'Rehearsal control path; model not invoked'
        : 'Failed closed at model boundary',
    authority: response.authority.final_decision_owner,
  }
}

function adapter(id: string, condition: Condition, fixture: AdapterResult): LiveDataAdapter<AdapterResult> {
  return {
    id,
    timeoutMs: 8_000,
    rehearsal: { data: fixture, collectedAt: '2026-09-28T12:00:00.000Z' },
    async load(signal) {
      const requestId = crypto.randomUUID()
      const response = await fetch('/api/v1/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Request-ID': requestId },
        body: JSON.stringify({
          schema_version: 'analysis-request/v1',
          request_id: requestId,
          origin: {
            kind: 'virtual-machine',
            namespace: 'virtualization-ai-101',
            vm_name: 'operations-vm',
            guest_hostname: 'operations-vm',
          },
          note: 'Operator note: intermittent vibration appears after restart and clears when load is reduced; inspect before the next production window.',
          allowed_categories: ['inspect', 'schedule-maintenance', 'escalate'],
          condition,
        }),
        signal,
      })
      if (!response.ok) throw new Error(`Live adapter returned HTTP ${response.status}`)
      const data = await response.json() as AnalysisResponse
      if (data.source_state !== 'LIVE') throw new Error(`Endpoint reported ${data.source_state}, not LIVE`)
      if (condition === 'healthy' && (!data.ai_participated || !data.model?.id)) {
        throw new Error('Healthy response did not prove model participation and identity')
      }
      if (condition === 'model-unavailable' && (data.ai_participated || data.result !== null)) {
        throw new Error('Unavailable response did not fail closed')
      }
      return flatten(data)
    },
  }
}

registerAdapter(adapter('vm-ai-healthy', 'healthy', healthyFixture))
registerAdapter(adapter('vm-ai-unavailable', 'model-unavailable', unavailableFixture))
