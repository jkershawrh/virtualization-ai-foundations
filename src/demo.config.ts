import type { DemoConfig } from './types'

const technicalTopology = {
  boundary: { label: 'OpenShift namespace', detail: 'virtualization-ai-101 workload boundary' },
  entry: { id: 'vm', kind: 'VirtualMachine / VMI', label: 'Operations VM', detail: 'originates the versioned request', endpoint: 'guest workload' },
  primaryPath: [
    { id: 'service', kind: 'v1 Service', label: 'ai-analysis', detail: 'stable namespace-local DNS', endpoint: ':8080', edgeLabel: 'HTTP JSON' },
    { id: 'adapter', kind: 'apps/v1 Deployment', label: 'AI analysis adapter', detail: 'validates input, output, identity, and source state', endpoint: 'POST /api/v1/analyze', edgeLabel: 'selects pod' },
    { id: 'model', kind: 'managed inference', label: 'Intel Xeon CPU model', detail: 'bounded interpretation of one synthetic note', endpoint: 'OpenAI-compatible HTTPS', edgeLabel: 'advisory inference' },
  ],
  supportPath: [
    { id: 'evidence', kind: 'evidence API', label: 'Correlated evidence', detail: 'request hash, origin, model, validation, and source state', endpoint: 'GET /api/v1/evidence/{id}', edgeLabel: 'same request ID' },
    { id: 'validation', kind: 'deterministic policy', label: 'Schema + category checks', detail: 'rejects malformed or out-of-policy model output', edgeLabel: 'validate' },
    { id: 'human', kind: 'authority', label: 'Human operator', detail: 'model is advisory; no actions are permitted', edgeLabel: 'review' },
  ],
}

export const demoConfig: DemoConfig = {
  id: 'virtualization-ai-foundations',
  title: 'Virtualization + AI 101',
  subtitle: 'Trace a VM-hosted workload to governed Intel Xeon CPU inference',
  event: 'Red Hat × Intel technical briefing',
  audience: 'Application owners, virtualization administrators, and platform engineers',
  cta: 'Trace the evidence. Keep the authority human.',
  brand: {
    primary: { name: 'Red Hat', logo: '/logos/redhat.svg', alt: 'Red Hat' },
    partner: { name: 'Intel', logo: '/logos/intel.png', alt: 'Intel' },
    attribution: 'Red Hat × Intel',
  },
  acts: [
    {
      id: 'decision', label: '00', title: 'The Decision', scenes: [
        {
          id: 'intro', type: 'intro', beat: 'ordinary-world',
          title: 'A VM and an AI service can share a platform—and still prove nothing.',
          subtitle: 'Coexistence is architecture. Trust requires evidence.',
          speakerPrompt: 'Open with the recognizable reality: established applications remain in VMs while AI arrives as a managed service. Do not claim savings, performance, or migration success.',
        },
        {
          id: 'reframe', type: 'reframe', beat: 'stakes', eyebrow: 'The reframe',
          title: 'Integration begins where the evidence chain begins',
          before: 'The VM and AI pod are both running',
          after: 'One request is attributable across every boundary',
          detail: 'Origin, Service routing, model participation, validation, failure state, and human authority must agree on the same request ID.',
          speakerPrompt: 'Name the exact gap in the old sources: the demos showed adjacency, but the automated evidence did not prove a request originated inside the guest.',
        },
      ],
    },
    {
      id: 'architecture', label: '01', title: 'Causal Architecture', scenes: [
        {
          id: 'guided-architecture', type: 'guided-architecture', beat: 'system-reveal', eyebrow: 'Guided architecture',
          title: 'Earn each boundary before showing the full path',
          body: 'One audience question reveals one runtime object, responsibility, protocol, and evidence source.',
          layers: [
            {
              id: 'origin', component: 'VirtualMachine / VMI', tone: 'primary',
              question: 'How do we know the request came from the established application?',
              answer: 'A checked-in client runs inside the operations VM and emits the request ID with guest identity.',
              detail: 'The guest receipt separates VM-origin evidence from a presenter, browser, or test-pod call.',
              activeNodeIds: ['vm'],
            },
            {
              id: 'network', component: 'OpenShift Service', tone: 'primary',
              question: 'How does the VM reach the AI capability without learning a pod address?',
              answer: 'Namespace-local Service DNS routes the versioned HTTP request to the adapter.',
              detail: 'NetworkPolicy permits only the VM launcher and presentation paths required by this journey.',
              activeNodeIds: ['vm', 'service'],
            },
            {
              id: 'adapter', component: 'AI analysis adapter', tone: 'success',
              question: 'Where are model credentials, schemas, and failure behavior governed?',
              answer: 'The adapter owns the credential boundary, deterministic validation, and evidence record.',
              detail: 'The VM never receives a model credential. Invalid or unavailable model output fails closed.',
              activeNodeIds: ['vm', 'service', 'adapter', 'validation', 'evidence'],
            },
            {
              id: 'inference', component: 'Intel Xeon CPU inference', tone: 'partner',
              question: 'What proves AI actually participated?',
              answer: 'A live response names the model, provider, Intel Xeon CPU hardware class, and source state.',
              detail: 'No model identity means no live AI claim. No authored latency, throughput, cost, or capacity appears here.',
              activeNodeIds: ['vm', 'service', 'adapter', 'model', 'evidence'],
            },
            {
              id: 'authority', component: 'Human operator', tone: 'primary',
              question: 'Who can act on the advisory result?',
              answer: 'Only the human operator; the model has no tools and no action authority.',
              detail: 'The response contract carries an empty actions-permitted list and a human final-decision owner.',
              activeNodeIds: ['vm', 'service', 'adapter', 'model', 'evidence', 'validation', 'human'],
            },
          ],
          technicalTopology,
          speakerPrompt: 'Ask, pause, reveal. Distinguish the VM workload path, the model role, deterministic validation, and authority. Do not reveal the completed topology before the questions earn it.',
        },
      ],
    },
    {
      id: 'proof', label: '02', title: 'Live Proof', scenes: [
        {
          id: 'live-journey', type: 'live-journey', beat: 'live-proof', eyebrow: 'Current-session evidence',
          title: 'Run the same path under two consequential conditions',
          body: 'Healthy inference and controlled unavailability retain separate source state and evidence.',
          cta: 'Run the VM-origin journey',
          nodes: [
            { id: 'vm', label: 'Operations VM', detail: 'request origin', tone: 'primary' },
            { id: 'service', label: 'OpenShift Service', detail: 'network boundary', tone: 'primary' },
            { id: 'adapter', label: 'AI adapter', detail: 'contract + evidence', tone: 'success' },
            { id: 'model', label: 'Xeon CPU model', detail: 'advisory inference', tone: 'partner' },
            { id: 'human', label: 'Human operator', detail: 'final authority', tone: 'primary' },
          ],
          technicalTopology,
          steps: [
            {
              id: 'healthy', title: 'Healthy model condition',
              detail: 'The adapter accepts a VM-shaped request only when the live endpoint returns model identity and schema-valid advisory output.',
              adapterId: 'vm-ai-healthy', activeNode: 4,
              activeNodeIds: ['vm', 'service', 'adapter', 'model', 'evidence', 'validation', 'human'],
              resultFields: [
                { key: 'source_state', label: 'Source state' },
                { key: 'ai_participated', label: 'AI participated' },
                { key: 'model_id', label: 'Model' },
                { key: 'hardware', label: 'Hardware' },
                { key: 'category', label: 'Advisory category' },
                { key: 'authority', label: 'Final authority' },
              ],
            },
            {
              id: 'unavailable', title: 'Unavailable model condition',
              detail: 'The same adapter path returns no model and no advisory output while preserving the human authority boundary.',
              adapterId: 'vm-ai-unavailable', activeNode: 4,
              activeNodeIds: ['vm', 'service', 'adapter', 'evidence', 'validation', 'human'],
              resultFields: [
                { key: 'source_state', label: 'Source state' },
                { key: 'ai_participated', label: 'AI participated' },
                { key: 'model_id', label: 'Model' },
                { key: 'outcome', label: 'Boundary result' },
                { key: 'category', label: 'Advisory category' },
                { key: 'authority', label: 'Final authority' },
              ],
            },
          ],
          speakerPrompt: 'Say LIVE, REHEARSAL, or OFFLINE before interpreting each result. Preserve the healthy result when running unavailability; the comparison is the proof.',
        },
        {
          id: 'decision-boundary', type: 'comparison', beat: 'trials',
          title: 'The boundary is the product of the proof',
          columns: [
            { label: 'Healthy condition', value: 'Advisory evidence', detail: 'Model identity plus deterministic validation can support a bounded human review.', tone: 'success' },
            { label: 'Unavailable condition', value: 'No invented answer', detail: 'The adapter exposes absence of model participation and returns no advisory result.', tone: 'partner' },
          ],
          speakerPrompt: 'The unavailable path is not a weaker demo. It proves that source state and authority survive when AI does not.',
        },
      ],
    },
    {
      id: 'mechanism', label: '03', title: 'Why It Holds', scenes: [
        {
          id: 'mechanisms', type: 'mechanisms', beat: 'trials', eyebrow: 'Mechanisms',
          title: 'Three controls make the evidence repeatable',
          mechanisms: [
            { id: 'contract', label: 'Versioned contract', claim: 'The VM and adapter agree before the model runs.', detail: 'Request, response, unavailable state, and evidence records are schema-bound.', tone: 'primary' },
            { id: 'provenance', label: 'Correlated provenance', claim: 'One request ID joins guest, Service, model, and validation evidence.', detail: 'The evidence record stores a request hash, not the raw note or a credential.', tone: 'partner' },
            { id: 'authority', label: 'Fail-closed authority', claim: 'A result can explain; it cannot act.', detail: 'The model has no tools, action list, or promotion authority. The human operator decides.', tone: 'success' },
          ],
          speakerPrompt: 'Keep mechanism depth inline. The lab will let learners inspect the actual contract and evidence record.',
        },
      ],
    },
    {
      id: 'payoff', label: '04', title: 'Evidence & Handoff', scenes: [
        {
          id: 'payoff', type: 'evidence-payoff', beat: 'transformation', eyebrow: 'What this session proved',
          title: 'Coexistence becomes credible when every boundary leaves evidence',
          adapterIds: ['vm-ai-healthy', 'vm-ai-unavailable'],
          fallbackLine: 'Run both proof conditions to populate the current-session payoff',
          evidenceFields: [
            { key: 'source_state', label: 'Latest source state' },
            { key: 'ai_participated', label: 'AI participated' },
            { key: 'outcome', label: 'Latest boundary result' },
            { key: 'authority', label: 'Final authority' },
          ],
          line1: 'The VM, Service, model, validation, and human authority stayed attributable.',
          line2: 'Trace it in 101. Build it in a separate 201.',
          cta: 'Close the presentation, then begin the 60–75 minute Showroom lab →',
          speakerPrompt: 'Recap only current-session evidence. If the source state is REHEARSAL or OFFLINE, say that the journey mechanics ran but live inference was not proven.',
        },
      ],
    },
  ],
  journeyHandoffs: [
    {
      depth: 'lab',
      title: 'Virtualization + AI 101 hands-on lab',
      duration: '60–75 minutes',
      question: 'Can the learner trace the same evidence and explain every authority boundary?',
      technology: 'OpenShift Virtualization · Service networking · Intel Xeon CPU inference · Showroom',
      instruction: 'Open the separate Showroom lab supplied by the environment. The future 201 lab will require learners to author the contract and configuration.',
    },
  ],
}
