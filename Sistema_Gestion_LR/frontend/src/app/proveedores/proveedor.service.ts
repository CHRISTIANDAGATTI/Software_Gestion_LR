import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProveedorService {
  private apiUrl = environment.apiUrl + '/api/v1';

  constructor(private http: HttpClient) { }

  getProveedores(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/proveedores`);
  }

  deleteProveedor(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/proveedores/${id}`);
  }

  createProveedor(proveedor: any) {
    return this.http.post(`${this.apiUrl}/proveedores`, proveedor);
  }

  getProveedor(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/proveedores/${id}`);
  }
}
