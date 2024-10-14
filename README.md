# pour avoir les ciné du Mans

lancer via docker

```bash
docker build -t cinemans .
docker run -p 5000:5001 cinemans
```

lancer l'applitation directement

```bash
python3 app.py
```

mettre à jour la BDD

```bash
cd modules
python3 update_db.py
```
