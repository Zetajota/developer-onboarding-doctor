// Servidor de demostración minimalista
const port = process.env.PORT || 4589;
console.log(`[OK] Servidor listo para escuchar en puerto ${port}`);
console.log(`[OK] DATABASE_URL: ${process.env.DATABASE_URL ? 'Configurada' : 'Faltante'}`);
