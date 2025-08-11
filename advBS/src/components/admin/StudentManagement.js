// src/components/admin/StudentManagement.js
import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faEdit, faTrash, faSpinner } from '@fortawesome/free-solid-svg-icons';
import { userService } from '../../services/api';

const StudentManagement = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formError, setFormError] = useState(null);

  const [showForm, setShowForm] = useState(false);
  const [currentStudent, setCurrentStudent] = useState(null); // Para identificar se é edição
  const [searchTerm, setSearchTerm] = useState('');

  // Estado inicial do formulário
  const initialFormData = {
    name: '', // Nome real do usuário
    username: '', // Nome de usuário único
    email: '',
    password: '',
  };
  const [formData, setFormData] = useState(initialFormData);

  // Buscar alunos da API
  const fetchStudents = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await userService.getAll();
      setStudents(data);
    } catch (e) {
      console.error("Erro ao buscar alunos:", e);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  // Filtrar alunos com base no termo de busca
  const filteredStudents = students.filter(student =>
    (student.name && student.name.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (student.username && student.username.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (student.email && student.email.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  // Manipular mudanças no formulário
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // Abrir formulário para adicionar novo aluno
  const handleAddStudent = () => {
    setCurrentStudent(null);
    setFormData(initialFormData);
    setShowForm(true);
    setFormError(null);
  };

  // Abrir formulário para editar aluno existente
  const handleEditStudent = (student) => {
    setCurrentStudent(student);
    setFormData({
      name: student.name || '',
      username: student.username || '',
      email: student.email || '',
      password: '', // Senha não é pré-preenchida por segurança
    });
    setShowForm(true);
    setFormError(null);
  };

  // Salvar aluno (novo ou editado) via API
  const handleSaveStudent = async (e) => {
    e.preventDefault();
    setFormError(null);

    if (!formData.name || !formData.username || !formData.email) {
      setFormError("Nome, Username e Email são obrigatórios.");
      return;
    }
    if (!currentStudent && !formData.password) { // Senha obrigatória apenas para novos alunos
        setFormError("Senha é obrigatória para novos alunos.");
        return;
    }

    const studentData = {
      name: formData.name,
      username: formData.username,
      email: formData.email,
      type: 'student', // Corrigido: usar 'type' em vez de 'role'
    };

    if (formData.password) {
      studentData.password = formData.password;
    }

    try {
      if (currentStudent && currentStudent.id) {
        // Editar aluno existente
        await userService.update(currentStudent.id, studentData);
      } else {
        // Criar novo aluno
        await userService.create(studentData);
      }

      fetchStudents(); // Recarrega a lista de alunos
      setShowForm(false);
      setCurrentStudent(null); // Limpa o estado de edição
    } catch (err) {
      console.error("Erro ao salvar aluno:", err);
      setFormError(err.message);
    }
  };

  // Excluir aluno via API
  const handleDeleteStudent = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este aluno? Esta ação não pode ser desfeita.')) {
      try {
        await userService.delete(id);
        fetchStudents(); // Recarrega a lista de alunos
      } catch (err) {
        console.error("Erro ao excluir aluno:", err);
        setError(err.message);
      }
    }
  };

  if (loading) {
    return (
      <div className="p-6 text-white flex justify-center items-center min-h-[300px]">
        <FontAwesomeIcon icon={faSpinner} spin size="3x" />
        <span className="ml-4 text-xl">Carregando alunos...</span>
      </div>
    );
  }

  if (error) {
    return <div className="p-6 text-red-500">Erro ao carregar alunos: {error}. Tente recarregar a página.</div>;
  }

  return (
    <div className="p-6 text-white min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-semibold text-red-400">Gestão de Alunos</h2>
        <button
          className="bg-red-400 hover:bg-red-500 text-white font-bold py-2 px-4 rounded transition-colors duration-150"
          onClick={handleAddStudent}
        >
          <FontAwesomeIcon icon={faPlus} className="mr-2" /> Novo Aluno
        </button>
      </div>

      <div className="mb-6">
        <input
          type="text"
          placeholder="Buscar aluno por nome, username ou email..."
          className="w-full bg-gray-500 text-white px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-300 placeholder-gray-300"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {filteredStudents.length === 0 && !loading && (
        <p className="text-gray-400 text-center py-4">Nenhum aluno encontrado.</p>
      )}

      {filteredStudents.length > 0 && (
        <div className="bg-gray-700 rounded-lg overflow-x-auto shadow-lg">
          <table className="w-full min-w-full">
            <thead className="bg-gray-500">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Nome</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Username</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Data de Cadastro</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Último Login</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-white uppercase tracking-wider">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-600">
              {filteredStudents.map(student => (
                <tr key={student.id} className="hover:bg-gray-600 transition-colors duration-150">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.username}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.email}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.register_date ? new Date(student.register_date).toLocaleDateString() : 'N/A'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-white">{student.last_login ? new Date(student.last_login).toLocaleString() : 'Nunca'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      className="text-blue-400 hover:text-blue-300 mr-3 transition-colors duration-150"
                      onClick={() => handleEditStudent(student)}
                      title="Editar Aluno"
                    >
                      <FontAwesomeIcon icon={faEdit} />
                    </button>
                    <button
                      className="text-red-400 hover:text-red-300 transition-colors duration-150"
                      onClick={() => handleDeleteStudent(student.id)}
                      title="Excluir Aluno"
                    >
                      <FontAwesomeIcon icon={faTrash} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Formulário de Aluno Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 p-6 rounded-lg w-full max-w-lg shadow-xl transform transition-all">
            <h3 className="text-xl font-semibold mb-6 text-poker-red">
              {currentStudent ? 'Editar Aluno' : 'Adicionar Novo Aluno'}
            </h3>
            
            <form onSubmit={handleSaveStudent}>
              {formError && <p className="text-red-500 mb-4 bg-red-900 bg-opacity-50 p-3 rounded">{formError}</p>}
              <div className="mb-4">
                <label htmlFor="name" className="block mb-1 text-sm font-medium text-gray-300">Nome Real</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-poker-red"
                  required
                />
              </div>

              <div className="mb-4">
                <label htmlFor="username" className="block mb-1 text-sm font-medium text-gray-300">Username</label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="Nome de usuário único (ex: joao_silva)"
                  className="w-full bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-poker-red"
                  required
                />
              </div>
              
              <div className="mb-4">
                <label htmlFor="email" className="block mb-1 text-sm font-medium text-gray-300">Email</label>
                <input 
                  type="email" 
                  id="email" 
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-poker-red" 
                  required 
                />
              </div>
              
              <div className="mb-6">
                <label htmlFor="password" className="block mb-1 text-sm font-medium text-gray-300">Senha</label>
                <input 
                  type="password" 
                  id="password" 
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder={currentStudent ? "Deixe em branco para não alterar" : "Senha obrigatória"}
                  className="w-full bg-gray-700 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-poker-red"
                  {...(currentStudent ? {} : { required: true })}
                />
                 {currentStudent && (
                  <small className="text-gray-400 block mt-1">Deixe em branco para não alterar a senha.</small>
                )}
              </div>
              
              <div className="flex justify-end pt-2 border-t border-gray-700">
                <button 
                  type="button" 
                  className="bg-gray-600 hover:bg-gray-500 text-gray-200 font-bold py-2 px-4 rounded mr-2 transition-colors duration-150"
                  onClick={() => { setShowForm(false); setCurrentStudent(null); }}
                >
                  Cancelar
                </button>
                <button 
                  type="submit" 
                  className="bg-poker-red hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition-colors duration-150"
                >
                  {currentStudent ? 'Salvar Alterações' : 'Adicionar Aluno'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentManagement;

