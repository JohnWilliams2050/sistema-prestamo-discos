export interface Disc {
  id: string;
  titulo: string;
  artista: string;
  genero: string;
  anio_lanzamiento: number | null;
  stock_total: number;
  stock_disponible: number;
}