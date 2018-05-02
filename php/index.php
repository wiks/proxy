<!DOCTYPE html>
<!--
To change this license header, choose License Headers in Project Properties.
To change this template file, choose Tools | Templates
and open the template in the editor.
-->
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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
    <div id="footer">
        phrase to find: wiks
    </div>
        </div>
    </body>

    <script src="staticOLD/js/foot.js"></script>
    <script src="staticOLD/js/mybootstrap.js"></script>    
</html>
