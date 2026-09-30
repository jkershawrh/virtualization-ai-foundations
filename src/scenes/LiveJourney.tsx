import { useEffect, useRef, useState } from 'react'
import { getAdapter } from '../live/adapters'
import { runProof } from '../live/proof'
import type { LiveJourneyScene, ProofState } from '../types'
import { SceneFrame } from './SceneFrame'
import { TechnicalTopology } from './TechnicalTopology'

export function LiveJourney({ scene }: { scene: LiveJourneyScene }) {
  const [stepIndex, setStepIndex] = useState(-1)
  const [state, setState] = useState<ProofState>({ status: 'idle' })
  const [results, setResults] = useState<Record<string, ProofState>>({})
  const [showTopology, setShowTopology] = useState(false)
  const controller = useRef<AbortController | undefined>(undefined)
  const step = stepIndex >= 0 ? scene.steps[stepIndex] : undefined
  const complete = stepIndex === scene.steps.length - 1 && state.status === 'ready'

  useEffect(() => () => controller.current?.abort(), [])

  async function runStep(index: number) {
    controller.current?.abort()
    controller.current = new AbortController()
    setStepIndex(index)
    setState({ status: 'loading' })
    const next = scene.steps[index]
    const adapter = getAdapter(next.adapterId)
    if (!adapter) {
      setState({ status: 'error', error: `Adapter not registered: ${next.adapterId}` })
      return
    }
    const result = await runProof(adapter, controller.current.signal)
    setState(result)
    setResults((current) => ({ ...current, [next.id]: result }))
  }

  return <SceneFrame scene={scene}><div className="live-workspace" data-testid="live-workspace">
    <nav className="live-workspace-steps" aria-label="Live proof progress">
      {scene.steps.map((item, index) => <button key={item.id} disabled={index > stepIndex} className={index === stepIndex ? 'active' : index < stepIndex ? 'complete' : ''} onClick={() => index < stepIndex && void runStep(index)}><span>{index < stepIndex ? '✓' : index + 1}</span>{item.title}</button>)}
    </nav>
    <div className="live-workspace-main">
      <div className="journey-status">
        <small>{step ? `ACT ${stepIndex + 1} OF ${scene.steps.length}` : 'LIVE WORKLOAD'}</small>
        <strong>{step?.title ?? 'Start with the workload—not the topology'}</strong>
        <span>{step?.detail ?? 'Run a concrete input, then inspect the evidence and measurements returned by each condition.'}</span>
        {state.source && <span className={`source-badge source-${state.source}`}>{state.source}</span>}
      </div>
      {!step && <div className="live-workspace-intake">
        <span>INPUT · BOUNDED REQUEST</span>
        <strong>One synthetic operations note, one attributable origin</strong>
        <div className="intake-facts">
          <div><small>Origin</small><b>Operations VM</b></div>
          <div><small>Contract</small><b>analysis-request/v1</b></div>
          <div><small>Conditions</small><b>healthy → unavailable</b></div>
        </div>
        <blockquote>“Intermittent vibration appears after restart and clears when load is reduced; inspect before the next production window.”</blockquote>
        <small>No customer data, credential, action request, or authored performance claim enters the path.</small>
      </div>}
      {!scene.technicalTopology && step && <div className="live-architecture" aria-label="Live architecture journey">
      {scene.nodes.map((node, index) => <div className="live-node-wrap" key={node.id}>
        <div className={`live-node ${node.tone ? `tone-${node.tone}` : ''} ${step && index <= step.activeNode ? 'done' : ''} ${step?.activeNode === index ? 'active' : ''}`}>
          <strong>{node.label}</strong>{node.detail && <span>{node.detail}</span>}
        </div>
        {index < scene.nodes.length - 1 && <div className={`live-edge ${step && index < step.activeNode ? 'done' : ''}`}>→</div>}
      </div>)}
      </div>}
    <div className="journey-evidence-stack" aria-label="Accumulated proof conditions">
      {scene.steps.map((item, index) => {
        const result = results[item.id]
        if (!result || result.status !== 'ready' || !result.data || index > stepIndex) return null
        return <section className="journey-condition" key={item.id}>
          <header><strong>{item.title}</strong><span className={`source-badge source-${result.source ?? 'rehearsal'}`}>{result.source ?? 'not run'}</span></header>
          <div className="journey-results">
            {item.resultFields.map((field) => <div className="journey-result" key={field.key}><span>{field.label}</span><strong>{String(result.data?.[field.key] ?? '—')}{field.suffix}</strong></div>)}
          </div>
        </section>
      })}
    </div>
    {state.error && <p className="fallback-note">{state.error}{state.status === 'ready' ? ' Showing clearly labeled fallback evidence.' : ''}</p>}
      <div className="journey-controls">
      {scene.technicalTopology && <button className="button button-secondary" onClick={() => setShowTopology((visible) => !visible)}>{showTopology ? 'Hide' : 'Inspect'} technical topology</button>}
      {stepIndex < 0 && <button className="button button-primary" onClick={() => runStep(0)}>{scene.cta}</button>}
      {stepIndex >= 0 && !complete && state.status !== 'loading' && <button className="button button-primary" onClick={() => runStep(stepIndex + 1)}>Next live act →</button>}
      {state.status === 'loading' && <button className="button button-primary" disabled>Running…</button>}
      {state.status === 'error' && <button className="button button-secondary" onClick={() => runStep(stepIndex)}>Retry</button>}
      {complete && <button className="button button-secondary" onClick={() => { setStepIndex(-1); setState({ status: 'idle' }); setResults({}); setShowTopology(false) }}>Replay</button>}
      {complete && scene.workspace && <a className="button button-primary" href={scene.workspace.href}>{scene.workspace.label} →</a>}
      </div>
    </div>
    <aside className="live-workspace-context"><span>HOW IT WORKS</span><strong>Evidence accumulates</strong><p>Each action runs the configured adapter. Results stay attached to their source state, and later conditions do not erase earlier proof.</p><small>Any LLM participation must appear beside LIVE output that proves it.</small></aside>
  </div>
  {showTopology && scene.technicalTopology && <div className="live-topology-drawer"><TechnicalTopology topology={scene.technicalTopology} activeIds={step?.activeNodeIds ?? []} /></div>}
  </SceneFrame>
}
