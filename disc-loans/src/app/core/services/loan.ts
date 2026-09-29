import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { Renta, RentaCreate } from '../../models/renta';

interface RentaResource {
	data: { id: string; attributes: Omit<Renta, 'id'> };
}

@Injectable({ providedIn: 'root' })
export class LoanService {
	private readonly baseUrl = 'http://localhost:8000/rentas/';

	constructor(private http: HttpClient) {}

	create(renta: RentaCreate): Observable<Renta> {
		return this.http.post<RentaResource>(this.baseUrl, renta).pipe(
			map(({ data }) => ({ id: data.id, ...data.attributes })),
		);
	}
}
