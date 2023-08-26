<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="robots" content="noindex">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>stapidoc</title>
</head>
<body>
    <script>
        setTimeout(() => {
            const decode = (b64) => decodeURIComponent(atob(b64));
            const s_b64 = '${s_b64}';
            const ll_b64 = [
            % for l_b64 in ll_b64:
                '${l_b64}',
            % endfor
            ];
            document.querySelector('html').innerHTML = decode(s_b64);
            document.body.style['visibility'] = 'hidden';

            const links = [];
            for (let i = 0; i < ll_b64.length; i++)
                links.push(document.createElement('link'));
            document.head.append(...links);
            for (let i = 0; i < ll_b64.length; i++)
                links[i].outerHTML = decode(ll_b64[i]);

            setTimeout(() => {
                document.body.style['visibility'] = 'visible';
            }, 666);
        }, 334);
    </script>
</body>
</html>