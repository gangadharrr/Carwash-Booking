<?php


$con=mysqli_connect('localhost',"root","");

mysqli_select_db($con,"carwash");
$name=$_POST["user"];
$pass=$_POST["password"];
$s="select * from users where username='$name' && password='$pass'"; 
$result=mysqli_query($con,$s);
$num=mysqli_num_rows($result);

if($num==1){
    $_SESSION["username"]=$name;
    if($name=="Admin_GD"&& $pass=="Carwash@123")
    {
        header('location:AdminHome.php');
    }else{
    header('location:userhome.php');
}
}else{
    header("location:home.php");
}
?>
