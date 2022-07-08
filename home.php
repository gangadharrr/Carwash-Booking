<html>
    <head>
        <title>Login Page</title>
        <link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="Styles.css">
    </head>
    <body>
        <div class="container">
            <div class="login-box">
                <div class="row">
                    <div class="col-md-6 login-left">
                        <h2> Login </h2>
                        <form action="validation.php" method="POST">
                            <div class="form-group">
                                <label>Username</label>
                                <input type="text" name="user" class="form-control" required>
                                
                            </div>
                            <div class="form-group">
                                <label>Password</label>
                                <input type="password" name="password" class="form-control" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Login</button>
                        </form>
                    </div>
                        <div class="col-md-6 login-right">
                            <h2> Sign Up </h2>
                            <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" method="POST">
                                <div class="form-group">
                                    <label>Username</label>
                                    <input type="text" name="user" class="form-control" required>
                                </div>
                                <div class="form-group">
                                    <label>Password</label>
                                    <input type="text" name="password" class="form-control" required>
                                </div>
                                <button type="submit" class="btn btn-primary">Sign up</button>
                            </form>
                        </div>
                    </div>
                </div>
        </div>
        <?php
            session_start();

            $con=mysqli_connect('localhost',"root","");
            mysqli_select_db($con,"carwash");
            if ($_SERVER["REQUEST_METHOD"] == "POST") {
                $name=$_POST["user"];
                $pass=$_POST["password"];
            }
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

    </body>
</html>