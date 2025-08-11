const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
      logLevel: 'debug',
      pathRewrite: {
        '^/api': '/api', // manter o /api no caminho
      },
      onError: function (err, req, res) {
        console.log('Proxy Error:', err);
      },
      onProxyReq: function (proxyReq, req, res) {
        console.log('Proxy Request:', req.method, req.url);
      },
      onProxyRes: function (proxyRes, req, res) {
        console.log('Proxy Response:', proxyRes.statusCode, req.url);
        // Adicionar headers CORS na resposta
        proxyRes.headers['Access-Control-Allow-Origin'] = '*';
        proxyRes.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS';
        proxyRes.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Content-Length, X-Requested-With';
      }
    })
  );
};
