# Diagrama de orquestación del agente

```mermaid
flowchart TD
    U[Usuario<br/>Streamlit UI] -->|Solicitud de devolución| A

    subgraph AGENTE[Agente LangChain]
        A[Percepción<br/>parsea intención] --> P[Planner<br/>reglas de prioridad]
        P -->|decide siguiente acción| T{Selecciona Tool}
    end

    subgraph TOOLS[Herramientas]
        T --> T1[consultar_pedido]
        T --> T2[validar_politica]
        T --> T3[buscar_casos_similares<br/>RAG Chroma]
        T --> T4[calcular_reembolso]
        T --> T5[generar_etiqueta]
        T --> T6[actualizar_crm]
        T --> T7[notificar_cliente]
    end

    subgraph MEM[Memoria]
        M1[(Corto plazo<br/>session buffer)]
        M2[(Largo plazo<br/>SQLite)]
        M3[(Semántica<br/>Chroma)]
    end

    T1 & T2 & T3 --> M2 & M3
    T1 & T2 & T4 & T5 & T6 & T7 --> M1

    T -->|observación| R[Reasoning<br/>Gemini Flash]
    R -->|¿caso resuelto?| D{Decisión}
    D -->|No, requiere más pasos| P
    D -->|Sí, resuelto| F[Respuesta final<br/>+ actualizar estado]
    D -->|Requiere humano| E[Escalar<br/>+ justificar]
    F & E --> U

    style P fill:#ffe1b3
    style R fill:#b3d9ff
    style D fill:#ffb3b3
```

## Cómo leer el diagrama
1. El usuario escribe su solicitud en la interfaz Streamlit.
2. El agente la percibe y el **planner** aplica las 6 reglas de negocio en orden de prioridad.
3. Según la regla activada, se seleccionan y ejecutan una o más **tools** (consulta, escritura o razonamiento/RAG).
4. Cada tool lee o escribe en alguna de las tres capas de **memoria** (corto plazo, largo plazo en SQLite, semántica en Chroma).
5. El resultado vuelve como observación; si el caso está resuelto, se entrega una respuesta final (aprobación) o se escala a un humano con justificación trazable.

## Flujo de decisión (replanificación)
```mermaid
flowchart LR
    S[Solicitud] --> R1{¿Elegible?}
    R1 -- No --> ESC[Escalar]
    R1 -- Sí --> R2{¿Monto > 100.000?}
    R2 -- Sí --> APR[Solicitar aprobación]
    R2 -- No --> R3{¿≥3 devoluciones 90d?}
    R3 -- Sí --> FRA[Escalar por fraude]
    R3 -- No --> R4{¿Recurrente y monto < 50.000?}
    R4 -- Sí --> PREF[Aprobar preferente]
    R4 -- No --> R5{¿Falta info?}
    R5 -- Sí --> INFO[Solicitar info]
    R5 -- No --> STD[Aprobar estándar]
```
