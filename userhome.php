
<html>
    <head>
        <title>Home Page</title>
      
    </head>
  

    <body style="background-image:url(carwash.jpg); background-size:100%;">
        <style>
            .logout{
                float: right;
                padding-right: 20px;
            
                        text-decoration: none;
            }
            .right{
                background-color: skyblue;
                        border:1px solid blue;
                        
            }
            li{
                display: inline;
                padding: 10px 25px;
            }
            .user{
                margin-left: 400px;
                border-style:groove;
                margin-right: 400px;
                padding-left: 20px;
                
                background-color: white;
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
  <li> <a class="logout" href="logout.php"> LOGOUT </a></li>
        </ul></div>
<br><br><br>
   <div class="user">
    <h1 style="text-align: center;">Car Wash Booking</h1>
    <form method="POST">
        <label for="city">Select City Name:</label>
        <select id="city_sel"name="city_sel">
            
            <option value="0">-select-</option>
            <?php 
            session_start();
            $con=mysqli_connect('localhost',"root","");
            mysqli_select_db($con,"carwash");
            $s="select distinct cities from bodyshops"; 
            $result = mysqli_query($con, $s);
            $num=mysqli_fetch_all($result);
            foreach($num as $val){
                foreach($val as $vl)
                {
                    $x=$vl;?>
                    <option value=<?php echo $x;?>><?php echo $x;?></option><?php
                }
            }
            $con -> close(); 
            ?>
        </select><br><br>

        <label> Select Location:</label>
        <select id="loc_sel"name="loc_sel">
            
            <option value="0">-select-</option>
            <?php 
            $con=mysqli_connect('localhost',"root","");
            mysqli_select_db($con,"carwash");
            $s="select distinct locations from bodyshops"; 
            $result = mysqli_query($con, $s);
            $num=mysqli_fetch_all($result);
            foreach($num as $val){
                foreach($val as $vl)
                {
                    $x=$vl;?>
                    <option value=<?php echo $x;?>><?php echo $x;?></option><?php
                }
            }
            $con -> close(); 
            ?>
        </select><br><br>
        <label>Select Body_shop_name:</label>
        <select id="body_sel"name="body_sel">
            
            <option value="0">-select-</option>
            <?php 
            session_start();
            $con=mysqli_connect('localhost',"root","");
            mysqli_select_db($con,"carwash");
            $s="select distinct bodyshopname from bodyshops"; 
            $result = mysqli_query($con, $s);
            $num=mysqli_fetch_all($result);
            foreach($num as $val){
                foreach($val as $vl)
                {
                    $x=$vl;?>
                    <option value=<?php echo $vl;?>><?php echo $x;?></option><?php
                }
            }
            $con -> close(); 
            ?>
        </select><br><br>
        <label>Phone number:</label>
        <input type="text" name="phone"></input><br><br>
        <label>Model name:</label>
        <input type="text" name="model"></input><br><br>
        <button class="btn btn-primary" type="submit" name="submit">Submit</button>
    </form>
    <?php
        $con=mysqli_connect('localhost',"root","");
        mysqli_select_db($con,"carwash");
        error_reporting(E_ALL ^ E_NOTICE); 
        $city=$_POST["city_sel"];
        $loc=$_POST["loc_sel"];
        $bshop=$_POST["body_sel"];
        $phone=$_POST["phone"];
        $model=$_POST["model"];
        $s="select * from bookings where cities='$city' && locations='$loc'&& bodyshopname='$bshop'"; 
        $result=mysqli_query($con,$s);
        $num=mysqli_num_rows($result);
        if($num<=5){
        $reg="insert into bookings values ('$city','$loc','$bshop','$phone','$model')";
        mysqli_query($con,$reg);
        echo " Booking Successful";
        }
        else{        echo " Booking UNSuccessful";
        }
        $con -> close(); 
    ?>
    </div>

    </body>
</html>

