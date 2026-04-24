-- Enable RLS on all tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.services ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.client_cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.favorites ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.consultations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.process_files ENABLE ROW LEVEL SECURITY;
-- Assuming these tables exist based on application code
ALTER TABLE public.case_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.document_requests ENABLE ROW LEVEL SECURITY;

-- Helper function to check if user is admin
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS boolean AS $$
BEGIN
  RETURN (SELECT type FROM public.profiles WHERE id = auth.uid()) = 'admin';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- PROFILES POLICIES
CREATE POLICY "Profiles are viewable by owner and admins" ON public.profiles
  FOR SELECT USING (auth.uid() = id OR public.is_admin());

CREATE POLICY "Profiles are updatable by owner and admins" ON public.profiles
  FOR UPDATE USING (auth.uid() = id OR public.is_admin());

-- SERVICES POLICIES
CREATE POLICY "Services are viewable by everyone" ON public.services
  FOR SELECT USING (true);

CREATE POLICY "Services can only be managed by admins" ON public.services
  FOR ALL USING (public.is_admin());

-- CLIENT_CASES POLICIES
CREATE POLICY "Cases are viewable by owner and admins" ON public.client_cases
  FOR SELECT USING (user_id = auth.uid() OR public.is_admin());

CREATE POLICY "Cases can only be managed by admins" ON public.client_cases
  FOR ALL USING (public.is_admin());

-- CASE_EVENTS POLICIES
CREATE POLICY "Events are viewable by case owner and admins" ON public.case_events
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.client_cases
      WHERE id = case_id AND user_id = auth.uid()
    ) OR public.is_admin()
  );

CREATE POLICY "Events can only be created by admins" ON public.case_events
  FOR ALL USING (public.is_admin());

-- DOCUMENT_REQUESTS POLICIES
CREATE POLICY "Requests are viewable by case owner and admins" ON public.document_requests
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.client_cases
      WHERE id = case_id AND user_id = auth.uid()
    ) OR public.is_admin()
  );

CREATE POLICY "Requests can only be managed by admins" ON public.document_requests
  FOR ALL USING (public.is_admin());

-- PROCESS_FILES POLICIES
CREATE POLICY "Files are viewable by case owner and admins" ON public.process_files
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.client_cases
      WHERE id = case_id AND user_id = auth.uid()
    ) OR public.is_admin()
  );

CREATE POLICY "Files can be uploaded by case owner and admins" ON public.process_files
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.client_cases
      WHERE id = case_id AND user_id = auth.uid()
    ) OR public.is_admin()
  );
