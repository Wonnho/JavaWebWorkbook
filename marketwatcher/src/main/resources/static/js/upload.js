async function uploadToServer (formObj) {
       console.log("upload to server....")
       console.log(formObj)

       // Axios/browser supplies the multipart boundary for FormData.
       const response = await axios.post('/upload', formObj);
       return response.data
}

async function removeFileToServer(uuid,fileName) {
         const response=await axios.delete( `/remove/${uuid}_${fileName}`)
         return response.data
}
