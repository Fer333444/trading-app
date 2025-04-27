// dbconnection.js
const mysql = require('mysql2');

const connection = mysql.createConnection({
  host: 'localhost',             
  user: 'root',                  
  password: '',                  
  database: 'mi_base_datos'      
});

connection.connect((err) => {
  if (err) {
    console.error('Error al conectar a la base de datos:', err);
    return;
  }
  console.log('Conexión exitosa a MySQL');
});

module.exports = connection;
	