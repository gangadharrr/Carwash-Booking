<?php
session_start();
header("location:home.php"); 
$con=mysqli_connect('localhost',"root","");
mysqli_select_db($con,"carwash");
$name=$_POST["user"];
$pass=$_POST["password"];
$pattern="@[A-Z]@";

$s="select * from users where username='$name'"; 
$result=mysqli_query($con,$s);
$num=mysqli_num_rows($result);

if($num==1){
    echo "Username Already Taken";}

if(preg_match("@[A-Z]@",$pass)&&preg_match("@[a-z]@",$pass)&&preg_match("@[0-9]@",$pass)&&preg_match("@[^\w]@",$pass)&&strlen($pass)>7){
    $reg="insert into users values ('$name','$pass')";
    mysqli_query($con,$reg);
    echo " Registration Successful";
}
else{echo "weak password";}



?>
