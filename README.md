# Bot de Tasas – Cauciones vs. Billeteras Virtuales

Este bot en **Python** monitorea automáticamente la tasa de **cauciones tomadoras** del mercado argentino (extraídas desde [InvertirOnline](https://iol.invertironline.com)) y las compara con las **tasas TNA ofrecidas por billeteras virtuales** (desde [billeterasvirtuales.com.ar](https://billeterasvirtuales.com.ar)).

Cuando detecta que la tasa de caución supera la de las billeteras o alcanza un umbral alto (por defecto 70%), envía alertas por correo electrónico configurables por el usuario.

---

## Características

- Extracción automática de tasas desde fuentes públicas.  
- Comparación de tasas en tiempo real.  
- Notificación por correo vía SMTP (Gmail).  
- Ejecución programada cada 30 minutos (configurable).  
- Totalmente compatible con Render.com y otros entornos cloud.

---

## Instalación local
1. Cloná el repositorio:
   ```bash
   git clone https://github.com/<tu_usuario>/bot_caucion.git
   cd bot_caucion

2. Instala dependencias:
    ```bash
    pip install requests beautifulsoup4 schedule
