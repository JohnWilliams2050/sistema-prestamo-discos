import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { Disc } from '../../models/disc';

interface DiscAttributes {
  titulo: string;
  artista: string;
  genero: string;
  anio_lanzamiento: number | null;
  stock_total: number;
  stock_disponible: number;
}

interface DiscCollectionResponse {
  data: Array<{ id: string; attributes: DiscAttributes }>;
}

interface DiscResourceResponse {
  data: { id: string; attributes: DiscAttributes };
}

@Injectable({ providedIn: 'root' })
export class DiscService {
  private baseUrl = 'http://localhost:8000/discos/';

  constructor(private http: HttpClient) {}

  list(): Observable<Disc[]> {
    return this.http.get<DiscCollectionResponse>(this.baseUrl).pipe(
      map(({ data }) => data.map(({ id, attributes }) => ({ id, ...attributes }))),
    );
  }

  get(id: string): Observable<Disc> {
    return this.list().pipe(
      map((discs) => {
        const disc = discs.find((item) => item.id === id);
        if (!disc) throw new Error(`Disc ${id} was not found`);
        return disc;
      }),
    );
  }

  create(disc: Omit<Disc, 'id' | 'stock_disponible'>): Observable<Disc> {
    return this.http.post<DiscResourceResponse>(this.baseUrl, disc).pipe(
      map(({ data }) => ({ id: data.id, ...data.attributes })),
    );
  }
}

export { DiscService as Disc };
