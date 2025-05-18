-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 18, 2025 at 07:48 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `medrec_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('4a1a3a9f4cb5');

-- --------------------------------------------------------

--
-- Table structure for table `disease`
--

CREATE TABLE `disease` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `is_ai_predicted` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `disease`
--

INSERT INTO `disease` (`id`, `name`, `description`, `is_ai_predicted`) VALUES
(1, 'Test Disease', 'This is a test disease for the chat system.', NULL),
(2, 'Rheumatoid Arthritis', 'AI Predicted Disease', NULL),
(3, 'COVID-19', 'AI Predicted Disease', NULL),
(4, 'Cervical spondylosis', 'AI Predicted Disease', 1),
(5, 'Psoriasis', 'AI Predicted Disease', 1),
(6, 'Peptic ulcer diseae', 'AI Predicted Disease', 1),
(7, 'Paralysis (brain hemorrhage)', 'AI Predicted Disease', 1),
(8, 'Gastroenteritis', 'AI Predicted Disease', 1),
(9, 'Chronic cholestasis', 'AI Predicted Disease', 1),
(10, 'Arthritis', 'AI Predicted Disease', 1);

-- --------------------------------------------------------

--
-- Table structure for table `medicine`
--

CREATE TABLE `medicine` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `dosage` varchar(100) DEFAULT NULL,
  `disease_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `medicine`
--

INSERT INTO `medicine` (`id`, `name`, `description`, `dosage`, `disease_id`) VALUES
(1, 'Ursodeoxycholic acid', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 9),
(2, 'Cholestyramine', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 9),
(3, 'Methotrexate', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 9),
(4, 'Corticosteroids', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 9),
(5, 'Liver transplant', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 9),
(6, 'Topical treatments', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 5),
(7, 'Phototherapy', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 5),
(8, 'Systemic medications', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 5),
(9, 'Biologics', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 5),
(10, 'Coal tar', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 5),
(11, 'Pain relievers', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 4),
(12, 'Muscle relaxants', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 4),
(13, 'Physical therapy', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 4),
(14, 'Neck braces', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 4),
(15, 'Corticosteroids', 'AI Recommended Medicine', 'Consult a doctor for proper dosage', 4);

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

CREATE TABLE `message` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `recipient_id` int(11) NOT NULL,
  `prediction_id` int(11) NOT NULL,
  `body` text NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `message`
--

INSERT INTO `message` (`id`, `sender_id`, `recipient_id`, `prediction_id`, `body`, `created_at`, `is_read`) VALUES
(2, 16, 15, 3, 'ow hi', '2025-04-12 20:22:01', 1),
(3, 15, 16, 5, 'hi doc', '2025-04-18 11:57:13', 1),
(4, 16, 15, 5, 'ow hi there', '2025-04-18 11:57:35', 1),
(5, 1, 16, 7, 'hi from the patient', '2025-05-17 11:56:01', 1),
(6, 15, 16, 20, 'jkjkjkhkkj', '2025-05-18 10:52:59', 1),
(7, 16, 15, 20, 'oh hi', '2025-05-18 17:40:35', 0),
(9, 17, 18, 25, 'hi don', '2025-05-18 17:48:15', 1);

-- --------------------------------------------------------

--
-- Table structure for table `prediction`
--

CREATE TABLE `prediction` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `disease_id` int(11) NOT NULL,
  `symptoms` text NOT NULL,
  `confidence` float NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_reviewed` tinyint(1) DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT NULL,
  `needs_attention` tinyint(1) DEFAULT NULL,
  `expert_notes` text DEFAULT NULL,
  `reviewed_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prediction`
--

INSERT INTO `prediction` (`id`, `user_id`, `disease_id`, `symptoms`, `confidence`, `created_at`, `updated_at`, `is_reviewed`, `is_approved`, `needs_attention`, `expert_notes`, `reviewed_by`) VALUES
(2, 15, 1, 'fatigue, sore_throat, difficulty_breathing', 0.85, '2025-04-12 20:12:29', '2025-04-12 20:12:29', 0, 0, 0, NULL, NULL),
(3, 15, 1, 'fatigue, sore_throat, difficulty_breathing', 0.85, '2025-04-12 20:21:12', '2025-04-12 20:21:17', 0, 0, 0, NULL, 16),
(4, 15, 1, 'headache, body_pain, difficulty_breathing', 0.85, '2025-04-18 10:43:01', '2025-04-18 10:43:01', 0, 0, 0, NULL, NULL),
(5, 15, 2, 'Belching,Bladder issues,Bleeding mole,Blisters,Bloating,Blood in stool,Body aches,Bone fractures,Bone pain,Bowel issues,Burning,Butterfly-shaped rash,Change in bowel habits,Change in existing mole,Chest discomfort', 0.0293318, '2025-04-18 11:55:56', '2025-04-18 11:57:07', 0, 0, 1, NULL, 16),
(6, 15, 3, 'Nausea,Neck stiffness,Nosebleeds,Numbness,Pain during urination,Reduced appetite,Stooped posture,Swelling,Swelling in ankles,Swollen joints,Vomiting', 0.0360377, '2025-04-18 11:58:47', '2025-04-18 11:58:47', 0, 0, 1, NULL, NULL),
(7, 1, 4, 'neck_pain,irritation_in_anus,pus_filled_pimples,nausea', 95.0207, '2025-05-17 11:55:32', '2025-05-17 11:55:50', 0, 0, 1, NULL, 16),
(8, 15, 5, 'blackheads,indigestion,breathlessness,silver_like_dusting,nausea', 47.5661, '2025-05-18 10:25:45', '2025-05-18 10:25:45', 0, 0, 1, NULL, NULL),
(9, 15, 6, 'dark_urine,abdominal_pain,diarrhoea,loss_of_appetite,headache', 58.2062, '2025-05-18 10:26:46', '2025-05-18 10:26:46', 0, 0, 1, NULL, NULL),
(10, 15, 7, 'altered_sensorium,spinning_movements,watering_from_eyes,weakness_of_one_body_side,excessive_hunger,extra_marital_contacts,dark_urine,pain_in_anal_region', 89.0761, '2025-05-18 10:27:01', '2025-05-18 10:27:01', 0, 0, 1, NULL, NULL),
(11, 15, 6, 'dark_urine,pain_during_bowel_movements,high_fever,abdominal_pain,swollen_legs', 87.0306, '2025-05-18 10:29:40', '2025-05-18 10:29:40', 0, 0, 1, NULL, NULL),
(12, 15, 8, 'diarrhoea,lethargy,pain_in_anal_region,family_history', 88.8746, '2025-05-18 10:29:51', '2025-05-18 10:29:51', 0, 0, 1, NULL, NULL),
(13, 15, 9, 'dizziness,nodal_skin_eruptions,headache,scurring', 20.2512, '2025-05-18 10:30:01', '2025-05-18 10:30:01', 0, 0, 1, NULL, NULL),
(14, 15, 9, 'chest_pain,burning_micturition,irregular_sugar_level,constipation', 20.25, '2025-05-18 10:30:07', '2025-05-18 10:30:07', 0, 0, 1, NULL, NULL),
(15, 15, 5, 'irritation_in_anus,movement_stiffness,cramps,pus_filled_pimples,indigestion,back_pain,breathlessness,stomach_pain,cold_hands_and_feets,silver_like_dusting,patches_in_throat,vomiting,anxiety,nausea,yellowish_skin,fatigue,weight_loss,obesity,knee_pain,swelling_of_stomach,joint_pain,loss_of_balance,dischromic__patches,chills,small_dents_in_nails,skin_peeling,altered_sensorium,spinning_movements,watering_from_eyes', 55.4981, '2025-05-18 10:30:21', '2025-05-18 10:30:21', 0, 0, 1, NULL, NULL),
(16, 15, 10, 'acidity,distention_of_abdomen,continuous_sneezing,stiff_neck,muscle_weakness', 60.8451, '2025-05-18 10:31:18', '2025-05-18 10:31:18', 0, 0, 1, NULL, NULL),
(17, 15, 9, 'irritation_in_anus,movement_stiffness,cramps,pus_filled_pimples', 20.2322, '2025-05-18 10:48:28', '2025-05-18 10:48:28', 0, 0, 1, NULL, NULL),
(18, 15, 9, 'blackheads,irritation_in_anus,movement_stiffness,cramps,pus_filled_pimples,indigestion', 20.2322, '2025-05-18 10:49:49', '2025-05-18 10:49:49', 0, 0, 1, NULL, NULL),
(19, 15, 5, 'skin_peeling,altered_sensorium,spinning_movements,watering_from_eyes', 45.7217, '2025-05-18 10:51:11', '2025-05-18 10:51:11', 0, 0, 1, NULL, NULL),
(20, 15, 5, 'cold_hands_and_feets,silver_like_dusting,patches_in_throat,vomiting', 46.2268, '2025-05-18 10:52:18', '2025-05-18 10:52:55', 0, 0, 1, NULL, 16),
(21, 15, 4, 'neck_pain,blackheads,irritation_in_anus,movement_stiffness', 79.4395, '2025-05-18 10:53:14', '2025-05-18 10:53:14', 0, 0, 1, NULL, NULL),
(22, 1, 9, 'blackheads,irritation_in_anus,movement_stiffness,cramps,pus_filled_pimples', 20.2322, '2025-05-18 11:00:49', '2025-05-18 11:00:49', 0, 0, 1, NULL, NULL),
(23, 1, 9, 'blackheads,irritation_in_anus,movement_stiffness,cramps,pus_filled_pimples,indigestion', 20.2322, '2025-05-18 17:24:05', '2025-05-18 17:24:05', 0, 0, 1, NULL, NULL),
(24, 17, 9, 'blackheads,irritation_in_anus,movement_stiffness,cramps,pus_filled_pimples,indigestion', 20.2322, '2025-05-18 17:45:06', '2025-05-18 17:45:13', 0, 0, 1, NULL, 16),
(25, 17, 4, 'foul_smell_of_urine,neck_pain,blackheads,irritation_in_anus,movement_stiffness', 79.4395, '2025-05-18 17:48:04', '2025-05-18 17:48:07', 0, 0, 1, NULL, 18);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(64) DEFAULT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(256) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `license_number` varchar(50) DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`, `full_name`, `specialization`, `license_number`, `is_approved`, `updated_at`) VALUES
(1, 'admin', 'admin@example.com', 'pbkdf2:sha256:600000$pCcKrL9o4iAN7fQY$ae14269b17f7434bad20506db1eecc7675abdca8976afd2ebc8a7b29b095c0d9', 'admin', NULL, 'Admin', NULL, NULL, NULL, '2025-05-18 17:23:54'),
(15, NULL, 'noba@gmail.com', 'pbkdf2:sha256:1000000$05cHsUf9JG9nxUBh$f842b365df5cf0735bd6f06e126e216a8fb5f3588e3ab122381a1bf5d8d340c5', 'patient', '2025-04-12 19:56:05', 'Nobel', NULL, NULL, 0, NULL),
(16, NULL, 'expert@gmail.com', 'pbkdf2:sha256:1000000$Ck72gvHdHYJejkOz$b369dc39c862b8543046f6db899d8c58f52d35138a217e16a6d4d0279207822f', 'medical_expert', '2025-04-12 19:56:33', 'Medical Expert', 'Medical Doctor', 'B-22865', 1, NULL),
(17, NULL, 'hafiz@gmail.com', 'pbkdf2:sha256:260000$USmmoYNra6GpEZlX$b075748ffd33b22853f6fe6bf73f059ef1b8ec91ea8cccb052f34fae3fcade90', 'patient', '2025-05-18 17:44:56', 'Hafizo', NULL, NULL, 0, '2025-05-18 17:44:56'),
(18, NULL, 'surgeon@example.com', 'pbkdf2:sha256:260000$o6GAUF8WPvMsFT58$5dac507807316616f51cbf4368535203698615084fdf6ca15b4df07520f11a53', 'medical_expert', '2025-05-18 17:46:41', 'Surgeon', 'Surgeon', '3836ddd', 1, '2025-05-18 17:46:41');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `disease`
--
ALTER TABLE `disease`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `medicine`
--
ALTER TABLE `medicine`
  ADD PRIMARY KEY (`id`),
  ADD KEY `disease_id` (`disease_id`);

--
-- Indexes for table `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `prediction_id` (`prediction_id`),
  ADD KEY `recipient_id` (`recipient_id`),
  ADD KEY `sender_id` (`sender_id`);

--
-- Indexes for table `prediction`
--
ALTER TABLE `prediction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `disease_id` (`disease_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `reviewed_by` (`reviewed_by`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `disease`
--
ALTER TABLE `disease`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `medicine`
--
ALTER TABLE `medicine`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `message`
--
ALTER TABLE `message`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `prediction`
--
ALTER TABLE `prediction`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `medicine`
--
ALTER TABLE `medicine`
  ADD CONSTRAINT `medicine_ibfk_1` FOREIGN KEY (`disease_id`) REFERENCES `disease` (`id`);

--
-- Constraints for table `message`
--
ALTER TABLE `message`
  ADD CONSTRAINT `message_ibfk_1` FOREIGN KEY (`prediction_id`) REFERENCES `prediction` (`id`),
  ADD CONSTRAINT `message_ibfk_2` FOREIGN KEY (`recipient_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `message_ibfk_3` FOREIGN KEY (`sender_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `prediction`
--
ALTER TABLE `prediction`
  ADD CONSTRAINT `prediction_ibfk_1` FOREIGN KEY (`disease_id`) REFERENCES `disease` (`id`),
  ADD CONSTRAINT `prediction_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `prediction_ibfk_3` FOREIGN KEY (`reviewed_by`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
