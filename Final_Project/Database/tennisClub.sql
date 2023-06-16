-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主机： localhost:8889
-- 生成日期： 2023-06-16 07:18:39
-- 服务器版本： 5.7.39
-- PHP 版本： 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `tennisClub`
--

-- --------------------------------------------------------

--
-- 表的结构 `Challenge`
--

CREATE TABLE `Challenge` (
  `CID` int(11) NOT NULL,
  `ChallengerMEID` int(11) NOT NULL,
  `ChallengedMEID` int(11) NOT NULL,
  `DateOfChallenge` date NOT NULL,
  `Status` int(1) DEFAULT NULL,
  `Notes` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `Member`
--

CREATE TABLE `Member` (
  `MEID` int(11) NOT NULL,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `Email` varchar(50) NOT NULL,
  `MPassword` varchar(30) NOT NULL,
  `Phone` varchar(20) NOT NULL,
  `Age` int(11) NOT NULL,
  `Gender` varchar(10) NOT NULL,
  `UTR` float NOT NULL,
  `DateOfCreation` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `Membership`
--

CREATE TABLE `Membership` (
  `MSID` int(11) NOT NULL,
  `MEID` int(11) NOT NULL,
  `StartDate` date NOT NULL,
  `EndDate` date NOT NULL,
  `InvoiceDate` date NOT NULL,
  `DueDate` date NOT NULL,
  `Amount` decimal(10,0) NOT NULL,
  `PaidDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `TMatch`
--

CREATE TABLE `TMatch` (
  `MAID` int(11) NOT NULL,
  `CID` int(11) DEFAULT NULL,
  `DataOfMatch` date NOT NULL,
  `MEID1Set1Score` int(1) NOT NULL,
  `MEID2Set1Score` int(1) NOT NULL,
  `MEID1Set2Score` int(1) DEFAULT NULL,
  `MEID2Set2Score` int(1) DEFAULT NULL,
  `MEID1Set3Score` int(1) DEFAULT NULL,
  `MEID2Set3Score` int(1) DEFAULT NULL,
  `WinnerMEID` int(11) DEFAULT NULL,
  `LoserMEID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转储表的索引
--

--
-- 表的索引 `Challenge`
--
ALTER TABLE `Challenge`
  ADD PRIMARY KEY (`CID`),
  ADD UNIQUE KEY `ChallengerMEID` (`ChallengerMEID`),
  ADD UNIQUE KEY `ChallengedMEID` (`ChallengedMEID`);

--
-- 表的索引 `Membership`
--
ALTER TABLE `Membership`
  ADD PRIMARY KEY (`MSID`);

--
-- 表的索引 `TMatch`
--
ALTER TABLE `TMatch`
  ADD PRIMARY KEY (`MAID`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `Challenge`
--
ALTER TABLE `Challenge`
  MODIFY `CID` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `Membership`
--
ALTER TABLE `Membership`
  MODIFY `MSID` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `TMatch`
--
ALTER TABLE `TMatch`
  MODIFY `MAID` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
