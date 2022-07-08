<?php
session_start();
?>
<html>
    <head>
        <title>Home Page</title>
    </head>
    <body style="background-image:url(carwash.jpg); background-size:100%;">
        <style>
            .right{
               background-color: skyblue;
               border:1px solid blue;

            }
            li{
             display: inline;
             padding-right: 30px;
             
           
            }
            .cities{
                padding: 10px 30px;
                margin-left: 400px;
                border-style:groove;
                margin-right: 400px;
                background-color: white;
               
            }
            .logout{
                text-decoration: none;
            }
            .btn-primary{
                padding: 10px 25px;
                background-color: skyblue;
            }
            .btn-primary:hover{
            background-color: orange;
            }
            
        </style>
        <div class="right">
        <ul>
      <li>  <a class="logout" href="AdminHome.php">ADD PLACES</a></li>
      <li>  <a class="logout" href="Adminbook.php">BOOKINGS</a></li>
  <li>  <a style="float:right; padding-right:20px;" class="logout" href="logout.php"> LOGOUT </a></li>
    </ul></div><br><br>
    <div class="cities">
        <h1 style="text-align:center;">Add Body Shop</h1>
        <form method="POST">
        <label for="city">Enter City:</label>
          <input type="text" name="city_name" required><br><br>
          <label for="Location">Enter Location City:</label>
          <input type="text" name="loc_name" required><br><br>
          <label for="shop">Enter Body Shop:</label>
          <input type="text" name="shop_name" required><br><br>
          <?php

            $con=mysqli_connect('localhost',"root","");

            mysqli_select_db($con,"carwash");
            error_reporting(E_ALL ^ E_NOTICE);  
            $city=$_POST["city_name"];
            $loc=$_POST["loc_name"];
            $bshop=$_POST["shop_name"];
            $s="select * from bodyshops where bodyshopname='$bshop' && locations='$loc' && cities='$city'"; 
            $result=mysqli_query($con,$s);
            $num=mysqli_num_rows($result);

            if($num==1){
                echo "Body shop Already Taken<br><br>";
            }else{
                $reg="insert into bodyshops values ('$city','$loc','$bshop')";
                mysqli_query($con,$reg);
                echo " Added Successful<br><br>";
            }
            mysqli_close($con);
            ?>
          <button type="submit" class="btn btn-primary">Submit</button>
          
        </form>
    </div>
    
    </body>
</html>

