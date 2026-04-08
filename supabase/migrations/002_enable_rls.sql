
-- Storage Policies for process-files bucket
-- Note: Bucket must be created via Supabase UI or CLI first
CREATE POLICY "Public Access to process-files" ON storage.objects
  FOR SELECT USING ( bucket_id = 'process-files' );

CREATE POLICY "Authenticated Uploads to process-files" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'process-files' 
    AND auth.role() = 'authenticated'
  );

CREATE POLICY "Admin Full Access to process-files" ON storage.objects
  FOR ALL USING (
    bucket_id = 'process-files' 
    AND (SELECT type FROM public.profiles WHERE id = auth.uid()) = 'admin'
  );
