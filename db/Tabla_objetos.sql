SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `objetos` (
    `id` int(11) NOT NULL,
    `nombre` varchar(45) NOT NULL,
  	`marca` varchar(45) NOT NULL,
  	`color` varchar(45) NOT NULL,
    `fragil` varchar(45) NOT NULL,
    `peso` varchar(45) NOT NULL,
  	`descripcion` varchar(225) NOT NULL,
  	`foto` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `objetos`(`id`, `nombre`, `marca`, `color`, `fragil`, `peso`, `descripcion`, `foto`) VALUES
(1, 'caja', 'Boxster', 'Cafe', 'No', '4', 'caja de tamaño 20 x 20 x 40, no contiene partes pequeñas', 'Caja.jpg');

ALTER TABLE `objetos`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `objetos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;