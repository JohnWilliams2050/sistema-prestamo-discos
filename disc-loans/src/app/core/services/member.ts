import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { Cliente, ClienteCreate } from '../../models/cliente';

interface ClienteResource {
	data: { id: string; attributes: Omit<Cliente, 'id'> };
}

@Injectable({ providedIn: 'root' })
export class MemberService {
	private readonly baseUrl = 'http://localhost:8000/clientes/';

	constructor(private http: HttpClient) {}

	findByEmail(email: string): Observable<Cliente> {
		return this.http.get<ClienteResource>(`${this.baseUrl}buscar`, { params: { email } }).pipe(
			map(({ data }) => ({ id: data.id, ...data.attributes })),
		);
	}

	create(cliente: ClienteCreate): Observable<Cliente> {
		return this.http.post<ClienteResource>(this.baseUrl, cliente).pipe(
			map(({ data }) => ({ id: data.id, ...data.attributes })),
		);
	}

	setActive(cliente: Cliente, active: boolean): Observable<Cliente> {
		const action = active ? 'activar' : 'desactivar';
		return this.http.patch<ClienteResource>(`${this.baseUrl}${cliente.id}/${action}`, {}).pipe(
			map(({ data }) => ({ id: data.id, ...data.attributes })),
		);
	}
}
