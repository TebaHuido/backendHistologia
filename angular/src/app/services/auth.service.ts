import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private baseUrl = 'http://localhost:8000/api'; // Cambia esto a tu URL de backend

  constructor(private http: HttpClient, private router: Router) {}

  login(username: string, password: string) {
    return this.http.post(`${this.baseUrl}/login/`, { username, password });
  }

  logout() {
    sessionStorage.removeItem('user');
    this.router.navigate(['/login']);
  }

  setUser(user: any) {
    sessionStorage.setItem('user', JSON.stringify(user));
  }

  getUser() {
    return JSON.parse(sessionStorage.getItem('user') || '{}');
  }

  isLoggedIn() {
    return !!sessionStorage.getItem('user');
  }
}
