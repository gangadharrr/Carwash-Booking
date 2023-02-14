-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 14, 2023 at 12:02 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `carwash`
--

-- --------------------------------------------------------

--
-- Table structure for table `accrejdb`
--

CREATE TABLE `accrejdb` (
  `cities` varchar(50) NOT NULL,
  `locations` varchar(50) NOT NULL,
  `bodyshopname` varchar(50) NOT NULL,
  `Phoneno` varchar(50) NOT NULL,
  `model` varchar(50) NOT NULL,
  `servicetype` varchar(50) NOT NULL,
  `userid` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `accrejdb`
--

INSERT INTO `accrejdb` (`cities`, `locations`, `bodyshopname`, `Phoneno`, `model`, `servicetype`, `userid`, `status`) VALUES
('Dehli', 'Redfort', 'PQR', '9444444444', '49498', 'Foam Wash', 'eswar', 'Accept'),
('Hyd', 'OldCity', 'ABC', 'dfhdghd', 'dfgdsgsd', 'Basic Wash', 'eswar', 'Accept');

-- --------------------------------------------------------

--
-- Table structure for table `bodyshops`
--

CREATE TABLE `bodyshops` (
  `cities` varchar(50) NOT NULL,
  `locations` varchar(50) NOT NULL,
  `bodyshopname` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bodyshops`
--

INSERT INTO `bodyshops` (`cities`, `locations`, `bodyshopname`) VALUES
('Chennai', 'Navlur', 'ABC'),
('Chennai', 'T-nagar', 'ABC'),
('Chennai', 'T-nagar', 'PQR'),
('Chennai', 'Navlur', 'XYZ'),
('Hyd', 'OldCity', 'ABC'),
('Hyd', 'Navlur', 'XYZ'),
('Dehli', 'Redfort', 'PQR'),
('Dehli', 'Redfort', 'KMN'),
('Mumbai', 'Navymumbai', 'XUR'),
('', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `cities` varchar(50) NOT NULL,
  `locations` varchar(50) NOT NULL,
  `bodyshopname` varchar(50) NOT NULL,
  `Phoneno` varchar(15) NOT NULL,
  `model` varchar(50) NOT NULL,
  `servicetype` varchar(50) NOT NULL,
  `userid` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `servicetype` varchar(50) NOT NULL,
  `price` int(4) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`servicetype`, `price`) VALUES
('Basic Wash', 240),
('Foam Wash', 300);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `password`) VALUES
('9a7174d1cf08b61c7bf9cafe287f4dce', 'b7a84f4452aa9d48aa8c0f43073bbd8d');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD UNIQUE KEY `servicetype` (`servicetype`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
