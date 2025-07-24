import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProveedorService {
  private apiUrl = 'http://127.0.0.1:8000/api/v1';

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
