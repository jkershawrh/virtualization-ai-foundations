{{- define "virtualization-ai.name" -}}
virtualization-ai-foundations
{{- end }}

{{- define "virtualization-ai.labels" -}}
app.kubernetes.io/name: {{ include "virtualization-ai.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/part-of: virtualization-ai-101
{{- end }}

{{- define "virtualization-ai.image" -}}
{{- $image := index . 0 -}}
{{- if $image.digest -}}
{{ printf "%s@%s" $image.repository $image.digest }}
{{- else -}}
{{ printf "%s:%s" $image.repository $image.tag }}
{{- end -}}
{{- end }}
