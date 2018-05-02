Uruchomienie
============

Uruchomienie poprzez:

    .. code-block:: python

        python __init__.py

program wykonuje się dość długo, wybiera jedne adres proxy i wysyła do niego zlecenie odwiedziny strony z settings,
która ECHOuje via PHP dane odebrane z servera proxy i zwraca do programu Pythona.
Ten sprawdza, czy w otrzymanej treści jest adres IP (ustawiony w settings - tabela DB) oraz fraza 'wiks' - która występuje na stronie.

Pomyślny test, gdy NIE znaleziono IP oraz ZNALEZONO 'wiks'

Timeout dla jednego proxy to 30 sekund -ustawiane w settings.

Wyniki w tabeli DB.


Skrypt PHP pod adresem: http://www.wiks.eu/ip


    .. code-block:: php

        <?php
            /** find IP
             *
             * @return type
             */
            function getUserIP() {

                $client  = @$_SERVER['HTTP_CLIENT_IP'];
                $forward = @$_SERVER['HTTP_X_FORWARDED_FOR'];
                $remote  = $_SERVER['REMOTE_ADDR'];

                if(filter_var($client, FILTER_VALIDATE_IP)) {
                    $ip = $client;
                }
                elseif(filter_var($forward, FILTER_VALIDATE_IP)) {
                    $ip = $forward;
                }
                else {
                    $ip = $remote;
                }
                return $ip;
            }
            $user_ip = getUserIP();
            $stack_ips = array();
            $stack_rest = array();
            foreach($_SERVER as $key => $value) {
                if( filter_var($value, FILTER_VALIDATE_IP)) {
                    $stack_ips[] = array($key, $value);
                }else{
                    $stack_rest[] = array($key, $value);
                }
            }
        ?>
        <html>
            <head>
                <meta charset="UTF-8">
                <title><?php echo $user_ip; ?></title>
            </head>
            <body>
                <div id="container">
            <div id="main">
                <h1>
                <?php echo 'IP: '.$user_ip; ?>
                </h1>
                <br>
                <table style="width: 100%; border: 1;">
                <?php
                foreach($stack_ips as $row) { ?>
                    <tr>
                    <td>
                    <?php echo $row['0']; ?>
                    </td>
                    <td>
                    <?php echo '<strong>'.$row['1'].'</strong>'; ?>
                    </td>
                    </tr>
                <?php }
                foreach($stack_rest as $row) {?>
                    <tr>
                    <td>
                    <?php echo $row['0']; ?>
                    </td>
                    <td>
                    <?php echo $row['1']; ?>
                    </td>
                    </tr>
                <?php }
                ?>
                </table>
            </div>
                </div>
            </body>
        </html>


Pośróð 600 sprawdzonych proxy, ok

.. automodule:: __init__
   :members:
