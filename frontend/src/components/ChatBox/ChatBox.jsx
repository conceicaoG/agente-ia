import React, { useState } from 'react';
import { Container, Form, Button, Spinner } from 'react-bootstrap';
import './ChatBox.css';

export default function ChatBox() {
  const [message, setMessage] = useState('');
  // const [setResponse] = useState('');
  const [loading, setLoading] = useState(false); // nova variável para controlar o "pensando"
  const [conversa, setConversa] = useState([]);

  const enviarMensagem = async () => {
  if (!message.trim()) return;

  setLoading(true);

  try {
    const res = await fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();

    setConversa((prev) => [
      ...prev,
      { tipo: 'usuario', texto: message },
      { tipo: 'ia', texto: data.resposta },
    ]);

    setMessage('');
  } catch (error) {
    setConversa((prev) => [
      ...prev,
      { tipo: 'usuario', texto: message },
      { tipo: 'ia', texto: 'Erro ao conectar com a IA.' },
    ]);
    setMessage('');
  } finally {
    setLoading(false);
  }
};

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault(); // evita quebra de linha no textarea
      enviarMensagem();
    }
  };

  

  return (
  <Container
    className="chatbox-container d-flex flex-column"
    style={{ maxWidth: '800px', height: '100vh', backgroundColor: '#f8f9fa', padding: '2rem', borderRadius: '8px' }}
  >
    <h2 className="chatbox-title text-center mb-4">Chat com IA</h2>

    <div
      className="chatbox-conversa mb-3"
      style={{
        flexGrow: 1,
        overflowY: 'auto',
        padding: '1rem',
        border: '1px solid #ccc',
        borderRadius: '8px',
        backgroundColor: '#fff'
      }}
    >
      {conversa.length === 0 && (
        <p className="text-center text-muted">Nenhuma mensagem enviada ainda.</p>
      )}

      {conversa.map((item, index) => (
        <div
          key={index}
          style={{
            textAlign: item.tipo === 'usuario' ? 'right' : 'left',
            marginBottom: '1rem',
          }}
        >
          <strong>{item.tipo === 'usuario' ? 'Você:' : 'IA:'}</strong>
          <p style={{ margin: 0 }}>{item.texto}</p>
        </div>
      ))}
    </div>

    <Form.Control
      as="textarea"
      rows={4}
      className="chatbox-textarea mb-3"
      value={message}
      onChange={(e) => setMessage(e.target.value)}
      onKeyDown={handleKeyDown}
      placeholder="Digite sua mensagem aqui..."
      disabled={loading}
    />

    <Button className="chatbox-button" onClick={enviarMensagem} variant="primary" disabled={loading}>
      {loading ? (
        <>
          <Spinner
            as="span"
            animation="border"
            size="sm"
            role="status"
            aria-hidden="true"
          /> Pensando...
        </>
      ) : (
        'Enviar'
      )}
    </Button>
  </Container>
);
}
