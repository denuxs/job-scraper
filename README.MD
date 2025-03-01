# Job Scraper

Aplicación Web que extrae ofertas laborales de los sitios web: encuentra24, computrabajo y tecoloco.

Desarrollado con fines educativos. La carga puede tomar algunos segundos por que esta alojado en la platadorma Render con plan gratuito.

### Paquetes

* Python 3
* BeautifulSoup
* Streamlit
* Selenium
* Pandas
* ThreadPoolExecutor

### Instalar y ejecutar app

Crear un entorno virtual con el paquete virtualenv
```
virtualenv -p python3 venv
source venv/bin/activate
```

Instalar los paquetes

```
pip install -r requirements.txt
```

Renombra el archivo .env.example a .env y modifica los valores de las variables

```
streamlit run main.py
```

### TO DO

* Refactorizar código
* Actualizar a Scrapy Framework
* Crear API con FastAPI