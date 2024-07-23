# Set the streaming parameters
stream = sl.StreamingParameters()
stream.codec = sl.STREAMING_CODEC.H264 # Can be H264 or H265
stream.bitrate = 8000
stream.port = 30000 # Port used for sending the stream
# Enable streaming with the streaming parameters
err = zed.enable_streaming(stream)

while not exit_app :
    zed.grab()

# Disable streaming
zed.disable_streaming()