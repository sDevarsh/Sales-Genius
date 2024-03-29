// file-upload.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UploadService {

  constructor(private http: HttpClient) { }

  uploadFile(file: File) {
    const formData = new FormData();
    formData.append('csvFile', file);
    return this.http.post<any>('http://localhost:3000/upload', formData);
  }
  sendStringArray(strings: string[]) {
    const apiUrl = 'http://localhost:3000/receive-strings';
    return this.http.post<any>(apiUrl, { strings });
  }
}