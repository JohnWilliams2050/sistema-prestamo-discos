export type EstadoRenta = 'activa' | 'devuelta';

export interface Renta {
  id: string;
  fecha_renta: string;
  fecha_limite_devolucion: string;
  fecha_devolucion_real: string | null;
  estado: EstadoRenta;
}

export interface RentaCreate {
  cliente_id: string;
  disco_id: string;
}