// test.js
const express = require('express');
const app = express();
const connection = require('./dbconnection.js');

app.use(express.json());
app.use(express.static('public'));

/* 
  Ruta POST /accounts para crear una cuenta.
  Se envían: broker, currency, capital, risk_default.
*/
app.post('/accounts', (req, res) => {
  const { broker, currency, capital, risk_default } = req.body;
  if (!broker || !currency || !capital || !risk_default) {
    return res.status(400).json({ error: 'Faltan campos para crear la cuenta.' });
  }
  const sql = `INSERT INTO accounts (broker, currency, capital, risk_default)
               VALUES (?, ?, ?, ?)`;
  connection.query(sql, [broker, currency, capital, risk_default], (error, results) => {
    if (error) {
      return res.status(500).json({ error: 'Error al crear la cuenta.' });
    }
    res.json({ mensaje: 'Cuenta creada con éxito', id: results.insertId });
  });
});

/* 
  Ruta GET /accounts para listar todas las cuentas.
*/
app.get('/accounts', (req, res) => {
  connection.query('SELECT * FROM accounts', (error, results) => {
    if (error) {
      return res.status(500).json({ error: 'Error al obtener las cuentas.' });
    }
    res.json(results);
  });
});

/*
  Ruta POST /calculate-compound para calcular el tamaño del lote con interés compuesto automático.
  Se esperan los siguientes datos en el body (JSON):
    - capitalInicial: Capital con el que se inició (o último capital positivo)
    - capitalActual: Capital actual (si es menor, se considera pérdida)
    - baseRisk: Riesgo base (porcentaje, por ejemplo, 1)
    - stopLossPips: Stop Loss en pips (por ejemplo, 20)
    - instrument: Par de divisas (ejemplo: "EURUSD")
*/
app.post('/calculate-compound', (req, res) => {
  const { capitalInicial, capitalActual, baseRisk, stopLossPips, instrument } = req.body;
  
  if (!capitalInicial || !capitalActual || !baseRisk || !stopLossPips || !instrument) {
    return res.status(400).json({ error: 'Faltan datos para el cálculo compuesto. Se requieren capitalInicial, capitalActual, baseRisk, stopLossPips e instrument.' });
  }
  
  const capInicial = parseFloat(capitalInicial);
  const capActual = parseFloat(capitalActual);
  const baseR = parseFloat(baseRisk);
  const sl = parseFloat(stopLossPips);
  
  if (capInicial <= 0 || capActual <= 0 || baseR < 0 || sl <= 0) {
    return res.status(400).json({ error: 'Los valores deben ser mayores a 0 y el riesgo base mayor o igual a 0.' });
  }
  
  // Calcular el factor de pérdida:
  // Si capitalActual es menor que capitalInicial, hay pérdidas.
  const factorPerdida = (capInicial - capActual) / capInicial;
  
  // Incremento del riesgo: por ejemplo, cada 10% de pérdida aumenta el riesgo en 0.5 puntos porcentuales.
  const incrementoRiesgo = factorPerdida * 5; // 10% de pérdida = 0.5% de incremento
  const riesgoEfectivo = baseR + incrementoRiesgo;
  
  // Calcular el monto a arriesgar, usando el capital actual y el riesgo efectivo.
  const montoRiesgo = capActual * (riesgoEfectivo / 100);
  
  // Determinar el valor monetario del pip:
  // Para pares sin "JPY", se asume que 1 pip en 1 lote estándar vale $10.
  // Para pares con "JPY", se asume que vale $100.
  let valorPip = 10;
  if (instrument.toUpperCase().includes('JPY')) {
    valorPip = 100;
  }
  
  // Calcular el tamaño del lote:
  // Lot Size = montoRiesgo / (stopLossPips * valorPip)
  const lotSize = montoRiesgo / (sl * valorPip);
  
  res.json({
    riesgoEfectivo: riesgoEfectivo.toFixed(2),
    montoRiesgo: montoRiesgo.toFixed(2),
    lotSize: parseFloat(lotSize.toFixed(2))
  });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor escuchando en el puerto ${PORT}`);
});
