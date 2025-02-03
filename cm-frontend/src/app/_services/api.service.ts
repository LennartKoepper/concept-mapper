import { HttpClient, HttpResponse, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { catchError, throwError } from 'rxjs';
import { Payload } from '../_shared/payload';
import { Options } from '../_shared/options';
import { saveAs } from 'file-saver';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  apiURL = environment.apiURL;

  constructor(private http: HttpClient) { }

  postText(text: string, options: Options): Observable<void> {
    var json: Payload = {payload: text, options: options}

    let headers = new HttpHeaders();
    headers.append('Content-Type', 'application/json');

    return this.http.post(this.apiURL + "/text", json, {headers: headers, observe:"response", responseType: "blob"}).pipe(
      catchError(err => this.handleError(err)),
      map(res => this.downloadFile(res, options))
    );
  }

  postFile(formData: FormData, options: Options):Observable<void> {
    let headers = new HttpHeaders();
    headers.append('Content-Type', 'multipart/form-data');
    formData.append("options", JSON.stringify(options))

    return this.http.post(this.apiURL + "/file-upload", formData, {headers: headers, observe:"response", responseType: "blob"}).pipe(
      catchError(err => this.handleError(err)),
      map(res => this.downloadFile(res, options))
    );
  }

  postURL(url: string, options: Options):Observable<void> {
    var json: Payload = {payload: url, options: options}

    let headers = new HttpHeaders();
    headers.append('Content-Type', 'application/json');

    return this.http.post(this.apiURL + "/url", json, {headers: headers, observe:"response", responseType: "blob"}).pipe(
      catchError(err => this.handleError(err)),
      map(res => this.downloadFile(res, options))
    );
  }

  private downloadFile(res: HttpResponse<Blob>, options: Options) {
    let filename = this.getFilename(res, options)
    saveAs(res.body!, filename)
  }

  private getFilename(res: HttpResponse<Blob>, options: Options) {
    // Extract filename from header
    const disposition = res.headers.get('Content-Disposition');
    const matches = disposition!.split(';').map(v => v.trim());
    let filename = matches!.find(v => v.startsWith('filename='))!.substring(9).replace(/"/g, '');

    // Handle optional extension override
    if (options && options.extension) {
      const ext = options.extension.startsWith('.') ? options.extension : `.${options.extension}`;
      filename = `${filename}${ext}`;
    }

    // Handle optional filename override 
    return options && options.filename ? options.filename : filename;
  }

  handleError(err: HttpErrorResponse) {
    let errorMessage = "An error occurred:\n";

    if (err.error && err.error.detail) {
        errorMessage += err.error.detail
    } else {
        errorMessage += `Status: ${err.status}\nMessage: ${err.message}`;
    }

    alert(errorMessage);
    return throwError(() => err);
  }
}
