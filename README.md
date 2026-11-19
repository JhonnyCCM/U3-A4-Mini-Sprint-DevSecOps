# Práctica Integradora U3-A4: Mini-Sprint DevSecOps

Repositorio oficial del **Grupo 7** para la práctica integradora de la asignatura **Ciclos de Desarrollo de Software Seguro** (ULEAM - Ingeniería de Software, 6to Nivel "A").

## Integrantes (Grupo 7)
- Castillo Mero Jhonny Cristhian
- García Reyes Robert Alejandro
- Ortiz García Carlos Luis

## Backlog de Seguridad del Sprint (Issues)
- **[US-SEC-01]** Eliminar `API_KEY` hardcodeada en `app.py` (usar `.env`) e implementar `pre-commit` con `detect-secrets`.
- **[US-SEC-02]** Remediar Inyección SQL (`CWE-89` / `Bandit B608`) en `POST /api/login` mediante consultas parametrizadas.
- **[US-SEC-03]** Generar inventario SBOM CycloneDX (`sbom.json`) y actualizar dependencias vulnerables con `pip-audit`.
- **[US-SEC-04]** Configurar Build Breaker en GitHub Actions con **Bandit (SAST)** y **pip-audit (SCA)**.

## Definition of Done (DoD) de Seguridad
1. **SAST limpio:** El código supera `bandit -r app.py -f txt` sin alertas de seguridad (exit code `0`).
2. **SCA limpio:** Las dependencias declaradas superan `pip-audit -r requirements.txt` sin CVEs conocidos (exit code `0`).
3. **Shift-Left local:** El código pasa el control local de `pre-commit` con `detect-secrets` sin secretos ni claves expuestas.
4. **Revisión por pares y CI:** Todo cambio se integra vía Pull Request aprobado por otro miembro del equipo y con check verde en el Build Breaker.
