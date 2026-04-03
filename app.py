# --- 4. VIDEO CENTER
elif tool_choice == "Video Center":
    st.header("🎥 Bulk Video Center")
    urls_input = st.text_area("Paste Video URLs (one per line):", placeholder="https://youtube.com/...")
    quality = st.selectbox("Select Quality", ["720p", "1080p", "4K", "MP3 Audio Only"])
    
    if st.button("Start Bulk Download"):
        if urls_input:
            urls_list = [u.strip() for u in urls_input.split('\n') if u.strip()]
            
            for url in urls_list:
                st.write(f"⏳ Processing: {url}")
                
                # --- STEP 1: DOWNLOAD TO SERVER (G: DRIVE) ---
                # Note: You will need a library like 'yt-dlp' here to actually get the file.
                # This is a placeholder path for the file your downloader creates:
                fake_file_path = os.path.join(DOWNLOADS_DIR, "video_result.mp4")
                
                # --- STEP 2: ADD THE DOWNLOAD BUTTON ---
                # This part sends the file from the G: drive to the user's phone/PC
                if os.path.exists(fake_file_path): 
                    with open(fake_file_path, "rb") as file:
                        st.download_button(
                            label=f"📥 Save Video to Device ({url[:30]}...)",
                            data=file,
                            file_name="craftify_download.mp4",
                            mime="video/mp4",
                            key=url # Unique key for each button in the loop
                        )
                else:
                    st.error("File not found on server. Ensure your downloader is saving to G:\Craftify_Studio\downloads")
        else:
            st.warning("Please enter URLs in bulk.")
