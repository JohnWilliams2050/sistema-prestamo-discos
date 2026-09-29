import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Disc } from '../../models/disc';

@Injectable({ providedIn: 'root' })
export class DiscService {
  private baseUrl = `${environment.apiUrl}/discs`;

  constructor(private http: HttpClient) {}

  list(): Observable<Disc[]> {
    return this.http.get<Disc[]>(this.baseUrl);
  }

  create(disc: Partial<Disc>): Observable<Disc> {
    return this.http.post<Disc>(this.baseUrl, disc);
  }
}
