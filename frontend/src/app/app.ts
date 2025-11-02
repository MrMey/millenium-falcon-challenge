import { Component, signal } from '@angular/core';
import { FileUpload } from './file-upload/file-upload';

@Component({
  selector: 'app-root',
  imports: [FileUpload,],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
}
