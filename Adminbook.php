<?php
session_start();
?>
<html>
    <head>
        <title>Home Page</title>
    </head>
    <body>
        <style>
            .cities{
                padding: 10px 20px;
                margin: 20px;
               
            }
            .right{
                background-color: skyblue;
               border:1px solid blue;
            }
            li{
             display: inline;
             padding-right: 30px;
            }
            .logout{
                text-decoration: none;
            }
            
        </style>
     <div class="right">
        <ul>
      <li>  <a class="logout" href="AdminHome.php">ADD PLACES</a></li>
      <li>  <a class="logout" href="Adminbook.php">BOOKINGS</a></li>
  <li>  <a style="float:right; padding-right:20px;" class="logout" href="logout.php"> LOGOUT </a></li>
    </ul></div>

    <div class="cities">
        <h1>Bookings</h1>
        <?php 
            $con=mysqli_connect('localhost',"root","");
            mysqli_select_db($con,"carwash");
            $s="select *  from bookings"; 
            $result = mysqli_query($con, $s);
            $num=mysqli_fetch_all($result);
            foreach($num as $val){
                foreach($val as $vl)
                {

                    echo $vl." ";
                }
                echo '<br>';
            }
            $con -> close(); 
        ?>
    </div>
    </body>
</html>
