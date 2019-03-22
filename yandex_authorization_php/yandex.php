<?

if (!$_GET['code']) {
	exit('eror code');
}


include 'config.php';

$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, 'https://oauth.yandex.ru/token');
curl_setopt($curl, CURLOPT_POST, 1);
curl_setopt($curl, CURLOPT_POSTFIELDS, 'grant_type=authorization_code&code='.$_GET['code'].'&client_id='.ID.'&client_secret='.SECRET);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
$token = json_decode(curl_exec($curl), true);
curl_close($curl);


$data = json_decode(file_get_contents('https://login.yandex.ru/info?oauth_token='.$token['access_token']), true);

echo '<pre>';
var_dump($data);
echo '</pre>';

?>