-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 01, 2018 at 09:26 PM
-- Server version: 5.5.59-0+deb8u1-log
-- PHP Version: 5.6.33-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `wiks_proxy`
--

-- --------------------------------------------------------

--
-- Table structure for table `all`
--

CREATE TABLE IF NOT EXISTS `all` (
`id` int(11) NOT NULL,
  `ipaddress` varchar(16) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `country` varchar(30) DEFAULT NULL,
  `dt_put` datetime DEFAULT NULL,
  `last_dt_success` datetime DEFAULT NULL,
  `last_success_time` int(11) DEFAULT NULL,
  `last_dt_porage` datetime DEFAULT NULL,
  `turnoff` tinyint(1) NOT NULL DEFAULT '0',
  `hiddedip` int(11) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `keyval`
--

CREATE TABLE IF NOT EXISTS `keyval` (
`id` int(11) NOT NULL,
  `key` varchar(20) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `dt` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `proxy_exceptions`
--

CREATE TABLE IF NOT EXISTS `proxy_exceptions` (
`id` int(11) NOT NULL,
  `ipaddress` varchar(16) COLLATE utf8_bin DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `id_exception` int(11) NOT NULL,
  `timeout` float DEFAULT NULL,
  `dt` datetime DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `proxy_kind_exceptions`
--

CREATE TABLE IF NOT EXISTS `proxy_kind_exceptions` (
`id` int(11) NOT NULL,
  `exception` text COLLATE utf8_bin,
  `dt` datetime DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `webbrowser_headers`
--

CREATE TABLE IF NOT EXISTS `webbrowser_headers` (
`id` int(11) NOT NULL,
  `user_agent` text COLLATE utf8_bin NOT NULL,
  `turnoff` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `all`
--
ALTER TABLE `all`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `keyval`
--
ALTER TABLE `keyval`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `proxy_exceptions`
--
ALTER TABLE `proxy_exceptions`
 ADD PRIMARY KEY (`id`), ADD KEY `id` (`id`);

--
-- Indexes for table `proxy_kind_exceptions`
--
ALTER TABLE `proxy_kind_exceptions`
 ADD PRIMARY KEY (`id`), ADD KEY `id` (`id`);

--
-- Indexes for table `webbrowser_headers`
--
ALTER TABLE `webbrowser_headers`
 ADD PRIMARY KEY (`id`), ADD KEY `id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `all`
--
ALTER TABLE `all`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `keyval`
--
ALTER TABLE `keyval`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `proxy_exceptions`
--
ALTER TABLE `proxy_exceptions`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `proxy_kind_exceptions`
--
ALTER TABLE `proxy_kind_exceptions`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `webbrowser_headers`
--
ALTER TABLE `webbrowser_headers`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
