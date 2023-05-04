import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import CloudUploadIcon from "@material-ui/icons/CloudUpload";
import TextField from "@material-ui/core/TextField";
import axios from "axios";
import Box from "@material-ui/core/Box";
// import image_icon from './src/image_icon' 

const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
      padding: "5px 10px"
    },
  },
  input: {
    display: "none",
  },
  center: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    // height: "100vh",
    // padding: "174px 10px"
    margin: "-43px -22px",
    padding: "115px 44px"
  },
}));

function ImageUploader() {
  const classes = useStyles();
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [prediction, setprediction] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    const reader = new FileReader();
    reader.onload = (event) => {
      setPreviewUrl(event.target.result);
    };
    reader.readAsDataURL(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post(
        "http://localhost:8000/files",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setResponse(response.data);
      setprediction(response.data)
      setSubmitted(true);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className={classes.center}>
      <div className="outer-box">
        <div className="image-preview-area">
          
          
          {!file ? (
            <img src={require('./image_icon.png')} width="200" className="image-icon"/>
          ) : null}
          {file ? (
            <img src={previewUrl} width="200" className="image-preview" />
          ) : null}
        </div>
        
        
        <Box boxShadow={3} p={3} className="main-box">
          <form className={classes.root} onSubmit={handleSubmit}>
            <input
              accept="image/*"
              className={classes.input}
              id="contained-button-file"
              multiple
              type="file"
              onChange={handleFileChange}
            />
            <label htmlFor="contained-button-file">
              <Button
                variant="contained"
                color="primary"
                startIcon={<CloudUploadIcon />}
                component="span"
              >
                Upload
              </Button>
            </label>
            <TextField
              id="outlined-read-only-input"
              label="Selected file"
              defaultValue="No file selected"
              InputProps={{
                readOnly: true,
              }}
              variant="outlined"
              value={file ? file.name : "No file selected"}
            />
            <Button variant="contained" color="primary" type="submit">
              Analyse
            </Button>
            
            
          </form>
          {submitted ? (
          <div className="result-area">
            <h1 className="result-text">{prediction}</h1>
          </div>
          ) : null}
        </Box>
      </div>

    </div>
  );
}

export default ImageUploader;