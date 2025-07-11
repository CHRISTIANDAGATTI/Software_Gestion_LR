import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StockService {
  private apiUrl = 'http://127.0.0.1:8000/api/v1'; // Tu backend FastAPI

  constructor(private http: HttpClient) { }


  // Productos
  getProducto(id?: number): Observable<any|any[]> {
    if (id !== undefined) {
      return this.http.get<any>(`${this.apiUrl}/productos/${id}`);
    }
    return this.http.get<any[]>(`${this.apiUrl}/productos`);
  }

  updateProducto(id: number, producto: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/productos/${id}`, producto);
  }

  deleteProducto(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/productos/${id}`);
  }

  // Categoría
  getCategoria(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/categorias`);
  }
  updateCategoria(id: number, categoria: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/categorias/${id}`, categoria);
  }

  deleteCategoria(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/categorias/${id}`);
  }
}

