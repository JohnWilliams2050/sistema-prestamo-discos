export type EstadoCliente = 'activo' | 'inactivo';

export interface Cliente {
  id: string;
  nombre: string;
  email: string;
  telefono: string | null;
  estado: EstadoCliente;
}

export interface ClienteCreate {
  nombre: string;
  email: string;
  telefono: string | null;
}