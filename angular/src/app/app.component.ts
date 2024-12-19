import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { RouterModule } from '@angular/router';
import { AuthService } from './services/auth.service';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterModule, CommonModule], 
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private authService: AuthService) {}

  isLoggedIn(): boolean {
    return this.authService.isLoggedIn();
  }

  isProfesor(): boolean {
    return this.authService.isProfesor();
  }

  logout(): void {
    this.authService.logout();
  }

  [x: string]: any;
  selectCategory(arg0: string) {
    throw new Error('Method not implemented.');
  }
  title = 'myapp';
}
