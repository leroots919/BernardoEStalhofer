import React, { useState } from 'react';
import Card from '../shared/Card';
import Button from '../shared/Button';

const DocumentUpload = ({ caseId, onUploadSuccess }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [description, setDescription] = useState('');
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const allowedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg',
    'image/jpg',
    'image/png',
    'text/plain',
    'application/zip',
    'application/x-rar-compressed'
  ];

  const handleFileSelect = (file) => {
    if (file && allowedTypes.includes(file.type)) {
      setSelectedFile(file);
    } else {
      alert('Tipo de arquivo não permitido. Use: PDF, DOC, DOCX, JPG, PNG, TXT, ZIP, RAR');
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Selecione um arquivo primeiro');
      return;
    }

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append('document', selectedFile);
      formData.append('description', description);
      if (caseId) {
        formData.append('case_id', caseId);
      }

      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/upload/document', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      const data = await response.json();

      if (response.ok) {
        alert('Arquivo enviado com sucesso!');
        setSelectedFile(null);
        setDescription('');
        if (onUploadSuccess) {
          onUploadSuccess(data);
        }
      } else {
        alert(data.error || 'Erro ao enviar arquivo');
      }
    } catch (error) {
      console.error('Erro no upload:', error);
      alert('Erro ao enviar arquivo');
    } finally {
      setUploading(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <Card className="p-6">
      <h3 className="text-xl font-bold text-white mb-4">Upload de Documentos</h3>
      
      {/* Área de Drop */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive 
            ? 'border-blue-500 bg-blue-500/10' 
            : 'border-gray-600 hover:border-gray-500'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {selectedFile ? (
          <div className="space-y-2">
            <div className="text-4xl">📄</div>
            <p className="text-white font-medium">{selectedFile.name}</p>
            <p className="text-gray-400 text-sm">{formatFileSize(selectedFile.size)}</p>
            <Button 
              onClick={() => setSelectedFile(null)}
              variant="outline"
              size="sm"
            >
              Remover
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-6xl text-gray-500">📁</div>
            <div>
              <p className="text-white mb-2">Arraste arquivos aqui ou</p>
              <label className="cursor-pointer">
                <input
                  type="file"
                  className="hidden"
                  onChange={(e) => handleFileSelect(e.target.files[0])}
                  accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.txt,.zip,.rar"
                />
                <Button variant="outline">
                  Selecionar Arquivo
                </Button>
              </label>
            </div>
            <p className="text-gray-400 text-sm">
              Tipos permitidos: PDF, DOC, DOCX, JPG, PNG, TXT, ZIP, RAR
            </p>
          </div>
        )}
      </div>

      {/* Descrição */}
      <div className="mt-4">
        <label className="block text-gray-300 text-sm font-medium mb-2">
          Descrição (opcional)
        </label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Descreva o documento..."
          className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows="3"
        />
      </div>

      {/* Botão de Upload */}
      <div className="mt-6">
        <Button 
          onClick={handleUpload}
          disabled={!selectedFile || uploading}
          variant="primary"
          className="w-full"
        >
          {uploading ? 'Enviando...' : 'Enviar Documento'}
        </Button>
      </div>

      {/* Informações */}
      <div className="mt-4 p-4 bg-blue-800/20 rounded-lg border border-blue-700">
        <h4 className="font-semibold text-white mb-2">📋 Dicas importantes:</h4>
        <ul className="text-sm text-gray-300 space-y-1">
          <li>• Tamanho máximo: 10MB por arquivo</li>
          <li>• Mantenha os documentos organizados com descrições claras</li>
          <li>• Documentos enviados ficam seguros e criptografados</li>
          <li>• Nossa equipe será notificada sobre novos uploads</li>
        </ul>
      </div>
    </Card>
  );
};

export default DocumentUpload;
