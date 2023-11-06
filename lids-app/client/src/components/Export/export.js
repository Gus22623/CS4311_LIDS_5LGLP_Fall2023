/**
 * @author Alejandro Jaramillo
 * @version 1.0, 9/15/23
*/

import React, { useEffect } from 'react';

// Export Formats (Bare UI Only)
function Export({ onUpload }){
  return(
    <div style="text-align: center;">
      <h1 style="margin-top: 40px;"> Export Format </h1>
      <hr class="rounded" style="margin-bottom: 20px;"></hr>
      <div style="margin: 0 auto; width: 250px; display: block;">
        <button onClick={onUpload} style="padding-left: 50px; padding-right: 50px; padding-top: 10px; padding-bottom: 10px; margin-bottom: 10px;">
          CSV
        </button>
        <button onClick={onUpload} style="padding-left: 50px; padding-right: 50px; padding-top: 10px; padding-bottom: 10px; margin-bottom: 10px;">
          XML
        </button>
        <button onClick={onUpload} style="padding-left: 46px; padding-right: 45px; padding-top: 10px; padding-bottom: 10px; margin-bottom: 10px;">
          JSON
        </button>
      </div>
    </div>
  );
}

export default Export;