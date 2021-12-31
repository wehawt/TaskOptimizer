mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp taskopti_web.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

echo "FROM python" >> tempdir/Dockerfile
echo "RUN pip install flask" >> tempdir/Dockerfile

echo "COPY  ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY  ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY  taskopti_web.py /home/myapp/" >> tempdir/Dockerfile
echo "RUN pip install flask_sqlalchemy" >> tempdir/Dockerfile
echo "RUN pip install flask_marshmallow" >> tempdir/Dockerfile
echo "EXPOSE 8080" >> tempdir/Dockerfile

echo "CMD python3 /home/myapp/taskopti_web.py" >> tempdir/Dockerfile

cd tempdir
docker build -t taskopti_app .

docker run -t -d -p 8080:8080 --name taskopti_apprunning taskopti_app