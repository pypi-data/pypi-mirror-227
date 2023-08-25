from enum import Enum

class Application(Enum):
    """
    Enumeration with all MIME types for applications.
    """
    Atom =                                "application/atom+xml";
    Compress =                            "application/x-compress";
    Compressed =                          "application/x-compressed";
    DirectX =                             "application/directx";
    ElipsePortalDashboard =               "application/vnd.elipse.portal.dashboard";
    ElipsePortalDashboardThumbnail =      "application/vnd.elipse.portal.dashboard.thumbnail";
    ElipsePortalFolder =                  "application/vnd.elipse.portal.folder";
    Gtar =                                "application/x-gtar";
    Gzip =                                "application/x-gzip";
    InternetStream =                      "application/internet-property-stream";
    JavaArchive =                         "application/java-archive";
    Javascript =                          "application/x-javascript";
    Json =                                "application/json";
    MicrosoftAccess =                     "application/msaccess";
    MicrosoftAccess2 =                    "application/x-msaccess";
    MicrosoftExcel =                      "application/vnd.ms-excel";
    MicrosoftPowerpoint =                 "application/vnd.ms-powerpoint";
    MicrosoftWord =                       "application/msword";
    OctetStream =                         "application/octet-stream";
    OneNote =                             "application/onenote";
    Pdf =                                 "application/pdf";
    Postscript =                          "application/postscript";
    PerformanceMonitor =                  "application/x-perfmon";
    Rtf =                                 "application/rtf";
    ShockwaveFlash =                      "application/x-shockwave-flash";
    Silverlight =                         "application/x-silverlight-app";
    Tar =                                 "application/x-tar";
    Visio =                               "application/vnd.visio";
    Xaml =                                "application/xaml+xml";
    Zip =                                 "application/x-zip-compressed";

class Text(Enum):
    """
    Enumeration with all MIME types for text files.
    """
    Css =                                 "text/css";
    Html =                                "text/html";
    JScript =                             "text/jscript";
    Plain =                               "text/plain";
    RichText =                            "text/richtext";
    Scriptlet =                           "text/scriptlet";
    TabSeparatedValues =                  "text/tab-separated-values";
    VbScript =                            "text/vbscript";
    Xml =                                 "text/xml";

class Image(Enum):
    """
    Enumeration with all MIME types for image files.
    """
    Bmp =                                 "image/bmp";
    Gif =                                 "image/gif";
    Icon =                                "image/x-icon";
    Ief =                                 "image/ief";
    Jpeg =                                "image/jpeg";
    Pjpeg =                               "image/pjpeg";
    Png =                                 "image/png";
    Tiff =                                "image/tiff";

class Audio(Enum):
    """
    Enumeration with all MIME types for audio files.
    """
    Aiff =                                "audio/aiff";
    Basic =                               "audio/basic";
    Mid =                                 "audio/mid";
    Mpeg =                                "audio/mpeg";
    Wav =                                 "audio/wav";

class Video(Enum):
    """
    Enumeration with all MIME types for video files.
    """
    Mpeg =                                "video/mpeg";
    Quicktime =                           "video/quicktime";



