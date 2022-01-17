using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.IO;


public class webReqApi : MonoBehaviour
{

    void Start()
    {
        StartCoroutine(GetRequest("http://127.0.0.1:5000/unity"));
    }

    IEnumerator GetRequest(string uri)
    {

        // path to file
        string path = Application.streamingAssetsPath + "/data.txt";
        UnityWebRequest dataFile = UnityWebRequest.Get(path);
        yield return dataFile.SendWebRequest();

        WWWForm form = new WWWForm();

        form.AddField("name", "matan");
        form.AddField("frameCount", Time.frameCount.ToString());
        form.AddBinaryData("fileUpload", bytes, "screenShot.png", "image/png");
        form.AddBinaryData("dataFile", dataFile.downloadHandler.data, Path.GetFileName(path));

        using (UnityWebRequest www = UnityWebRequest.Post(uri, form))
        {
            yield return www.SendWebRequest();
            Debug.Log("SERVER: " + www.downloadHandler.text); // server response

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                Debug.Log("Form upload completed!");
            }
        }
    }
}