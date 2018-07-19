#Eventex

Sistema de Eventos encomendado pela Morena.

## Como desenvlover?

1. Clone o repositório.
2. Crie um virtualenv  com python 3.6.5
3. Ative o virtualenv.
4. Instale as dependecias.
5. Configure a instancia com o .env
6. Execute os testes.

```console
git clone git@github.com:rodrigomagalha/eventex.git wttd
cd wttd
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```

## Como fazer o deploy?
1. Crie uma uma instancia no heroku.
2. Envie a configuração para o heroku.
3. Defina uma SECRET_KEY segura para a instançia.
4. Defina DEBUG=False
5. Configure o serviço de email.
6. Envie o código para o heroku.

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroky confgi:set DEBUG=False
#configuro e-mail
git push heroku master --force  
```

